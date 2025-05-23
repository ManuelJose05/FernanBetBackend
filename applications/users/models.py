from django.contrib.auth.models import AbstractUser
from django.db import models

LEVELS = [
    ('RECLUTA', 'Recluta del Recreo'),
    ('ANALISTA', 'Analista en Proceso'),
    ('ESTRATEGA', 'Estratega Valiente'),
    ('EXPERTO', 'Experto en Predicciones'),
    ('LEYENDA', 'Leyenda de Fernando III'),
]


LEVEL_DICT = dict(LEVELS)

COURSES = [
    ('1', '1º ESO'),
    ('2', '2º ESO'),
    ('3', '3º ESO'),
    ('4', '4º ESO'),
    ('1B','1º Bachillerato'),
    ('2B','2º Bachillerato'),
]

class User(AbstractUser):
    email = models.EmailField(verbose_name='Email',null=False,unique=True)
    course = models.CharField(max_length=250,verbose_name='Curso',choices=COURSES,null=False)
    #level = models.CharField(max_length=250,choices=LEVELS,verbose_name='Nivel',default='RECLUTA')
    experience = models.IntegerField(default=100,verbose_name='XP')
    is_active = models.BooleanField(default=True,verbose_name='Activo')
    school_id = models.ForeignKey('school.School',on_delete=models.CASCADE,null=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def level(self):
        xp = self.experience
        if xp <= 100:
            key = 'RECLUTA'
        elif xp <= 200:
            key = 'ANALISTA'
        elif xp <= 300:
            key = 'ESTRATEGA'
        elif xp <= 400:
            key = 'EXPERTO'
        else:
            key = 'LEYENDA'
        return (key,LEVEL_DICT[key])