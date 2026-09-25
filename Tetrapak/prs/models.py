from django.db import models

# Create your models here.
# Extrusoura
class Extrusoura(models.Model):

    re = models.CharField(max_length=100, verbose_name='RE')
    data = models.DateField(auto_now_add=True)
    turno = models.CharField(max_length=2)
    maquina_rodando = models.CharField(max_length=100,verbose_name='Máquina Rodando')
    maquina_disponivel = models.CharField(max_length=100,verbose_name='Máquina Disponível')
    
    inicio = models.TimeField(null=False, blank=False, auto_now=True)
    fim = models.TimeField(null = True)

    detalhamento = models.CharField(max_length=1500, verbose_name='Detalhamento')
    
    class Meta:
        ordering = ['-data', '-inicio']

class AguaExtrusoura(models.Model):
    re = models.CharField(max_length=100, verbose_name='RE')
    data = models.DateField(auto_now_add=True)
    turno = models.CharField(max_length=2)
    cloro = models.FloatField()
    turbidez = models.FloatField()
    horario = models.TimeField(null=False, blank=False, auto_now=True)
    observacao = models.CharField(max_length=1500, verbose_name='Observação')

    class Meta:
        ordering = ['-data', '-horario']

class FechamentoTurno(models.Model):
    re = models.CharField(max_length=100, verbose_name='RE')
    data = models.DateField(auto_now_add=True)
    turno = models.CharField(max_length=2)
    fardo_virgem = models.IntegerField()
    fardo_laminado = models.IntegerField()
    fardo_total = models.IntegerField(editable = False, default=0)
    reversao = models.IntegerField()
    observacao = models.CharField(max_length=1500, verbose_name='Observação')

    def save(self, *args, **kwargs):
        self.fardo_total = (self.fardo_virgem or 0) + (self.fardo_laminado or 0)
        super(FechamentoTurno, self).save(*args, **kwargs)