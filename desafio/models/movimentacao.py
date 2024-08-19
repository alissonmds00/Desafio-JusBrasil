from django.db import models
from .processo import Processo

class Movimentacao(models.Model):
  id = models.AutoField(primary_key=True)
  data = models.DateField(null=False)
  processo = models.ForeignKey(Processo, on_delete=models.CASCADE)
  acao = models.TextField(null=False)
  
  def __str__(self):
    return f'Movimentação {self.id} do processo {self.processo.numero_do_processo}'