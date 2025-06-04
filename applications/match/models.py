from django.db import models
from applications.team.models import Team
from applications.school.models import School

MATCH_STATUS = [
    ('PROGRAMADO', 'Programado'),
    ('CURSO', 'En curso'),
    ('FINALIZADO', 'Finalizado'),
    ('POSPUESTO', 'Pospuesto'),
    ('CANCELADO', 'Cancelado'),
]

MATCH_RESULTS = [
    ('AWAY', 'Visitante'),
    ('HOME', 'Local'),
    ('DRAW', 'Empate'),
]

class Match(models.Model):
    local_team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='matches_as_local')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='matches_as_visitor')
    local_team_score = models.IntegerField(null=True,blank=True,default=0)
    away_team_score = models.IntegerField(null=True,blank=True,default=0)
    date = models.DateTimeField()
    status = models.CharField(choices=MATCH_STATUS,default='PROGRAMADO',max_length=30)
    referee = models.CharField(max_length=200,null=True,blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE,related_name='school')
    result = models.CharField(choices=MATCH_RESULTS,max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.local_team.nombre} vs {self.away_team.nombre} on {self.date.strftime('%Y-%m-%d %H:%M')}"
