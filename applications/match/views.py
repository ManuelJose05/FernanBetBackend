from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from applications.apuestaUsuario.models import ApuestaUsuario
from applications.match.models import Match
from applications.match.serializers import MatchSerializer
from applications.match.utils import validar_condicion, calcular_cuota_total, obtener_resultado_real


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=['get'])
    def getMatchList(self,request):
        matchs = Match.objects.all()
        serializer = MatchSerializer(matchs, many=True)

        return JsonResponse({
            'matchs': serializer.data,
            'total': len(matchs)
        },status=200)

    @action(detail=True, methods=['get'])
    def getMatchById(self, request, pk):
        try:
            match = Match.objects.get(id=pk)
        except Match.DoesNotExist:
            return JsonResponse({"message": "Match not found"}, status=404)

        serializer = MatchSerializer(match)
        return JsonResponse(serializer.data, status=200)

    @action(detail=False, methods=['patch'])
    def finishMatch(self, request):
        try:
            body = request.data
            match_id = body.get('id')
            goles_local = body.get('goles_local')
            goles_away = body.get('goles_away')

            if match_id is None or goles_local is None or goles_away is None:
                return JsonResponse({"message": "id, goles_local y goles_away son requeridos"}, status=400)

            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return JsonResponse({"message": "Match not found"}, status=404)

        # Actualizamos el partido
        match.local_team_score = goles_local
        match.away_team_score = goles_away

        match.result = obtener_resultado_real(match)

        match.status = 'FINALIZADO'
        match.save()

        # Procesamos apuestas asociadas a ese partido
        apuestas = ApuestaUsuario.objects.filter(conditions__match=match, settled=False).distinct()

        for apuesta in apuestas:
            todas_cumplidas = True
            for condicion in apuesta.conditions.all():
                resultado = validar_condicion(condicion, match)
                condicion.is_winner = resultado
                condicion.save()
                if not resultado:
                    todas_cumplidas = False

            apuesta.is_winner = todas_cumplidas
            apuesta.settled = True

            if todas_cumplidas:
                xp = int(apuesta.amount * calcular_cuota_total(apuesta))
                apuesta.user.xp += xp
                apuesta.user.save()

            apuesta.save()

        return JsonResponse({
            "message": f"Partido {match.id} finalizado. Apuestas procesadas."
        }, status=200)
