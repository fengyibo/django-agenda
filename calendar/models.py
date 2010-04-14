from django.db import models
from django.contrib.auth.models import User

class Citas(models.Model):
    cliente = models.CharField(max_length=200, verbose_name = 'Cliente')
    hora_ini = models.TimeField(verbose_name = 'Hora de inicio')
    hora_fin = models.TimeField(verbose_name = 'Hora final')
    trabajo_realizar = models.CharField(max_length=250, verbose_name = 'Trabajo a realizar' )
    fecha = models.DateField()
    
    def __unicode__(self):
        return self.cliente
    
    class Meta:
        verbose_name = 'Control de Citas'
        verbose_name_plural = 'Control de Citas'

class Calendar(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    public = models.BooleanField(default=False)
