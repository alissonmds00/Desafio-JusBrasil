from django.db import models

class Processo(models.Model):
  numero_do_processo = models.CharField(max_length=50, null=False)
  grau = models.IntegerField(default=1, null=False)
  classe = models.CharField(max_length=150, null=False)
  area = models.CharField(max_length=100, null=False)
  assunto = models.CharField(max_length=100, null=False)
  data_de_distribuicao = models.DateField()
  juiz = models.CharField(max_length=150)
  valor_da_acao = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
  partes = models.TextField(default='Nenhum envolvido encontrado')
  movimentacoes = models.TextField(default='Nenhuma ação encontrada')
  class Meta:
    unique_together = ('numero_do_processo', 'grau')
  
  def __str__(self):
    return f"{self.numero_do_processo}/{self.grau}"