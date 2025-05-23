from django.db import models

class School(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nombre', null=False, blank=True)
    city = models.CharField(max_length=250, verbose_name='Ciudad', null=False, blank=True)
    postal_code = models.IntegerField(verbose_name='Postal', null=False, blank=True)
    address = models.CharField(max_length=250, verbose_name='Direccion', null=False, blank=True)
    email = models.EmailField(verbose_name='Email', null=False, unique=True)
    phone = models.IntegerField(verbose_name='Telefono', null=False, blank=True)

    def __str__(self):
        return self.name
