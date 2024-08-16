from django.db import models

class Processo(models.Model):
  numero_do_processo = models.CharField(max_length=50, unique=True, null=False)
  classe = models.CharField(max_length=150, null=False)
  area = models.CharField(max_length=100, null=False)
  assunto = models.CharField(max_length=100, null=False)
  data_de_distribuicao = models.DateField(null=False)
  juiz = models.CharField(max_length=150, null=False)
  valor_da_acao = models.DecimalField(max_digits=10, null=False, decimal_places=2)
  
  def __str__(self):
    return f"Processo {self.id}"

class Movimentacao(models.Model):
  id = models.AutoField(primary_key=True)
  data = models.DateField(null=False)
  movimento = models.CharField(max_length=2000)
  processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='movimentacoes')
  
  def __str__(self):
    return f'Movimentação {self.id}'
  
class Parte(models.Model):
  nome = models.CharField(max_length=255, null=False)
  tipo = models.CharField(max_length=50, null=False)
  
  def __str__(self):
    return f'Parte {self.nome}'
  
class ParteProcesso(models.Model):
  processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='processo_parte')
  parte = models.ForeignKey(Parte, on_delete=models.CASCADE, related_name='processo_parte')
  
  def __str__(self):
    return f'Parte {self.parte} no processo {self.processo}'
    
  