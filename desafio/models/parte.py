from django.db import models
from .processo import Processo

class Parte(models.Model):
  nome = models.CharField(max_length=255, null=False)
  funcao = models.CharField(max_length=50, null=False)
  processo = models.ForeignKey(Processo, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'Parte {self.nome}'