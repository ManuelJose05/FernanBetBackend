from django.db import models

from applications.match.models import PlayerMatchStat, Match
from applications.player.models import Player
from applications.users.models import User

TIPO_APUESTA = [
    ('match','Partido'),
    ('player','Jugador'),
]

STAT_TYPE = [
    ('GOL', 'Gol'),
    ('ASISTENCIA', 'Asistencia'),
    ('ROJA', 'Roja'),
    ('AMARILLA', 'Amarilla'),
    ('RESULTADO','Resultado')
]


class ApuestaUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    settled = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class CondicionApuesta(models.Model):
    apuesta = models.ForeignKey(ApuestaUsuario, on_delete=models.CASCADE,related_name='conditions')
    type = models.CharField(max_length=50, choices=TIPO_APUESTA)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    predicted_result = models.CharField(max_length=10, blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE,null=True,blank=True)
    stat_type = models.CharField(max_length=50, choices=STAT_TYPE)
    predicted_value = models.IntegerField(blank=True, null=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"Condición ({self.type}) para apuesta #{self.apuesta.id}"

    def evaluate(self) -> bool:
        if self.type == 'match':
            return self.predicted_result == self.match.result

        elif self.type == 'player' and self.player and self.stat_type:
            valor_real = (
                PlayerMatchStat.objects
                .filter(match=self.match, player=self.player, stat_type=self.stat_type)
                .values_list('value', flat=True)
                .first()
            )

            return valor_real == self.predicted_value if valor_real is not None else False

        return False