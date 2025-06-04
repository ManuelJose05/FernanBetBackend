from applications.apuestaUsuario.utils import get_cuota_de_condicion


def calcular_cuota_total(apuesta):
    total = 1
    for condicion in apuesta.conditions.all():
        total *= get_cuota_de_condicion(condicion)
    return round(total, 2)


def obtener_resultado_real(match):
    if match.local_team_score > match.away_team_score:
        return 'LOCAL'
    elif match.local_team_score < match.away_team_score:
        return 'AWAY'
    else:
        return 'DRAW'


def validar_condicion(condicion):
    player = condicion.player

    if condicion.stat_type == 'GOL':
        return condicion.player and player.goles < (player.goles + condicion.predicted_value)
    elif condicion.stat_type == 'ASISTENCIA':
        return condicion.player and condicion.player.asistencias >= condicion.predicted_value
    elif condicion.stat_type == 'ROJA':
        return condicion.player and condicion.player.rojas >= condicion.predicted_value
    elif condicion.stat_type == 'AMARILLA':
        return condicion.player and condicion.player.amarillas >= condicion.predicted_value
    elif condicion.stat_type == 'RESULTADO':
        match = condicion.match
        resultado_real = obtener_resultado_real(match)
        return resultado_real == condicion.predicted_result
    return False
