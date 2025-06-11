# def get_cuota_de_condicion(condicion):
#     player = condicion.player
#
#     if condicion.stat_type == 'RESULTADO':
#         partido = condicion.match
#         equipo_local = partido.local_team
#         equipo_visitante = partido.away_team
#
#         puntos_local = getattr(equipo_local, 'puntos', 0)
#         puntos_visitante = getattr(equipo_visitante, 'puntos', 0)
#
#         diferencia = abs(puntos_local - puntos_visitante)
#
#         if puntos_local > puntos_visitante:
#             cuota_local = 1.5 if diferencia < 5 else 1.2
#             cuota_away = 3.0 if diferencia < 5 else 4.0
#         elif puntos_visitante > puntos_local:
#             cuota_local = 3.0 if diferencia < 5 else 4.0
#             cuota_away = 1.5 if diferencia < 5 else 1.2
#         else:
#             cuota_local = cuota_away = 2.0
#
#         # Decidir qué cuota usar según lo que predijo el usuario
#         resultado = condicion.predicted_result
#
#         if resultado == 'LOCAL':
#             return cuota_local
#         elif resultado == 'AWAY':
#             return cuota_away
#         elif resultado == 'DRAW':
#             return 3.5
#         else:
#             return 2.0
#
#     if condicion.stat_type == 'GOL':
#         if not player:
#             return 3.0  # Cuota alta por falta de información
#         goles = player.goles or 0
#         if goles > 20:
#             return 1.5
#         elif goles >= 10:
#             return 2.0
#         else:
#             return 3.0
#
#     elif condicion.stat_type == 'ASISTENCIA':
#         if not player:
#             return 3.0
#         asistencias = player.asistencias or 0
#         if asistencias > 15:
#             return 1.7
#         elif asistencias >= 5:
#             return 2.2
#         else:
#             return 3.5
#
#     elif condicion.stat_type == 'ROJA':
#         if not player:
#             return 4.0
#         rojas = player.rojas or 0
#         if rojas >= 5:
#             return 1.8
#         elif rojas >= 2:
#             return 2.5
#         else:
#             return 4.0
#
#     elif condicion.stat_type == 'AMARILLA':
#         if not player:
#             return 2.5
#         amarillas = player.amarillas or 0
#         if amarillas >= 10:
#             return 1.8
#         elif amarillas >= 5:
#             return 2.2
#         else:
#             return 3.0
#
#     else:
#         return 1.5

def get_cuota_de_condicion(condicion):
    player = condicion.player

    if condicion.stat_type == 'RESULTADO':
        partido = condicion.match
        equipo_local = partido.local_team
        equipo_visitante = partido.away_team

        puntos_local = getattr(equipo_local, 'puntos', 0)
        puntos_visitante = getattr(equipo_visitante, 'puntos', 0)

        diferencia = abs(puntos_local - puntos_visitante)

        if puntos_local > puntos_visitante:
            cuota_local = 1.3 if diferencia < 5 else 1.1
            cuota_away = 2.2 if diferencia < 5 else 2.4
        elif puntos_visitante > puntos_local:
            cuota_local = 2.2 if diferencia < 5 else 2.4
            cuota_away = 1.3 if diferencia < 5 else 1.1
        else:
            cuota_local = cuota_away = 1.5

        resultado = condicion.predicted_result

        if resultado == 'LOCAL':
            return cuota_local
        elif resultado == 'AWAY':
            return cuota_away
        elif resultado == 'DRAW':
            return 2.2
        else:
            return 1.6

    if condicion.stat_type == 'GOL':
        if not player:
            return 2.2
        goles = player.goles or 0
        if goles > 20:
            return 1.2
        elif goles >= 10:
            return 1.6
        else:
            return 2

    elif condicion.stat_type == 'ASISTENCIA':
        if not player:
            return 2.2
        asistencias = player.asistencias or 0
        if asistencias > 15:
            return 1.3
        elif asistencias >= 5:
            return 1.7
        else:
            return 2

    elif condicion.stat_type == 'ROJA':
        if not player:
            return 2.8
        rojas = player.rojas or 0
        if rojas >= 5:
            return 1.4
        elif rojas >= 2:
            return 1.9
        else:
            return 2.2

    elif condicion.stat_type == 'AMARILLA':
        if not player:
            return 1.9
        amarillas = player.amarillas or 0
        if amarillas >= 10:
            return 1.4
        elif amarillas >= 5:
            return 1.8
        else:
            return 2

    else:
        return 1.2
