from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import condition
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from applications.apuestaUsuario.models import ApuestaUsuario
from applications.match.models import Match, PlayerMatchStat
from applications.match.serializers import MatchSerializer, MatchCreateSerializer
from applications.match.utils import validar_condicion, calcular_cuota_total, obtener_resultado_real
from applications.player.models import Player


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def createMatch(self, request):
        serializer = MatchCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def getMatchList(self, request):
        matchs = Match.objects.all()
        serializer = MatchSerializer(matchs, many=True)

        return JsonResponse({
            'matchs': serializer.data,
            'total': len(matchs)
        }, status=200)

    @action(detail=True, methods=['get'])
    def getMatchById(self, request, pk):
        try:
            match = Match.objects.get(id=pk)
        except Match.DoesNotExist:
            return JsonResponse({"message": "Match not found"}, status=404)

        serializer = MatchSerializer(match)
        return JsonResponse(serializer.data, status=200)

    @action(detail=False, methods=['post'])
    def finishMatch(self, request):
        body = request.data
        match_id = body.get('id')
        goles_local = body.get('goles_local')
        goles_away = body.get('goles_away')

        if None in (match_id, goles_local, goles_away):
            return JsonResponse(
                {"message": "id, goles_local y goles_away son requeridos"},
                status=400
            )

        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return JsonResponse({"message": "Match not found"}, status=404)

        with transaction.atomic():
            # 1) Actualizamos datos del partido
            match.local_team_score = goles_local
            match.local_team.gf += goles_local
            match.local_team.gc += goles_away
            match.local_team.pj += 1

            match.away_team_score = goles_away
            match.away_team.gf += goles_away
            match.away_team.gc += goles_local
            match.away_team.pj += 1

            match.result = obtener_resultado_real(match)
            if match.result == 'LOCAL':
                match.local_team.puntos += 3
                match.local_team.victorias += 1
                match.away_team.derrotas += 1
            elif match.result == 'AWAY':
                match.away_team.puntos += 3
                match.away_team.victorias += 1
                match.local_team.derrotas += 1
            else:
                match.local_team.empates += 1
                match.local_team.puntos += 1
                match.away_team.empates += 1
                match.away_team.puntos += 1

            match.local_team.save()
            match.away_team.save()

            match.status = 'FINALIZADO'
            match.save()

            # 2) Procesamos apuestas relacionadas a este partido
            apuestas = ApuestaUsuario.objects.filter(conditions__match=match, settled=False).distinct()

            for apuesta in apuestas:
                condiciones = apuesta.conditions.all()

                # Si alguna condición de esta apuesta depende de un partido aún no finalizado, saltamos
                if any(c.match.status != 'FINALIZADO' for c in condiciones):
                    continue

                todas_cumplidas = True
                for condicion in condiciones:
                    if condicion.evaluate():
                        condicion.is_winner = True
                        condicion.save(update_fields=['is_winner'])
                    else:
                        todas_cumplidas = False

                apuesta.settled = True
                apuesta.save(update_fields=['settled'])

                if todas_cumplidas:
                    xp = int(apuesta.amount * calcular_cuota_total(apuesta))
                    user = apuesta.user
                    user.experience += xp
                    user.save(update_fields=['experience'])

        return JsonResponse(
            {"message": f"Partido {match.id} finalizado. Apuestas procesadas."},
            status=200
        )

    @action(detail=True, methods=['post'])
    def updateMatchStats(self, request, pk=None):
        try:
            match = Match.objects.get(pk=pk)
        except Match.DoesNotExist:
            return JsonResponse({"message": "Match not found."}, status=404)

        goles_local = request.data.get('goles_local')
        goles_away = request.data.get('goles_away')
        stats = request.data.get('stats', [])

        if goles_local is None or goles_away is None or not isinstance(stats, list):
            return JsonResponse(
                {"message": "goles_local, goles_away y stats (list) son requeridos."},
                status=400
            )

        with transaction.atomic():
            # 1) Actualizar resultado del partido
            match.local_team_score = goles_local
            match.away_team_score = goles_away
            match.save(update_fields=['local_team_score', 'away_team_score'])

            # 3) Crear nuevas stats
            for stat in stats:
                player_id = stat.get('player_id')
                stat_type = stat.get('stat_type')
                value = stat.get('value')

                if None in (player_id, stat_type, value):
                    continue  # Ignora stats mal formadas

                try:
                    player = Player.objects.get(pk=player_id)
                    PlayerMatchStat.objects.update_or_create(
                        match=match,
                        player=player,
                        stat_type=stat_type,
                        defaults={'value': value}
                    )
                except Player.DoesNotExist:
                    continue  # Ignora si el jugador no existe

        return JsonResponse(
            {"message": f"Stats y resultado del partido {match.id} actualizados correctamente."},
            status=200
        )

    @action(detail=True, methods=['patch'])
    def updateMatchStatus(self, request, pk=None):
        status = request.data.get('status')

        if not status or not isinstance(status, str):
            return JsonResponse({"message": "status requeridos."}, status=400)
        try:
            match = Match.objects.get(pk=pk)
            match.status = status
            match.save(update_fields=['status'])
            return JsonResponse({"message": f"Partido {match.id} actualizado."}, status=200)
        except Match.DoesNotExist:
            return JsonResponse({"message": "Match not found."}, status=404)

