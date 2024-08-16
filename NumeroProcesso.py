import re
class NumeroProcesso:
  
  def __init__(self, numero):
    if len(numero) < 20:
      raise ValueError('Código inválido')
    numero_processo = self.validar_numero(numero)
    if (numero_processo):
      self._numero = numero_processo
      self._codigo_estado = self.obter_estado(numero_processo)
  
  @property
  def numero(self):
      return self._numero
      
  @property
  def codigo_estado(self):
      return self._codigo_estado
      
  def limpar_numero(self, numero):
    caracteres_especiais = r'[-.\s]'
    numero_limpo = re.sub(caracteres_especiais, '', numero)
    return numero_limpo
  
  def formatar_numero(self, numero):
      if len(numero) != 20 or not numero.isdigit():
          raise ValueError("O número deve ter exatamente 20 dígitos.")
      regex = r"(\d{7})(\d{2})(\d{4})(\d)(\d{2})(\d{4})"
      regex_final = r"\1-\2.\3.\4.\5.\6"
      numero_formatado = re.sub(regex, regex_final, numero)
      return numero_formatado
    
  def validar_numero(self, numero):
     numero_limpo = self.limpar_numero(numero)
     return self.formatar_numero(numero_limpo)
      
  def obter_estado(self, codigo):
    regex = r'^\d{7}-\d{2}\.\d{4}\.\d\.(\d{2})\.\d{4}$'
    match = re.search(regex, codigo)
    if match:
      return match.group(1)
    else:
      return None
    

codigo = NumeroProcesso('0710802-55.2018.8.02.0001')
codigo2 = NumeroProcesso('0070337-91.2008.8.06.0001')
print(vars(codigo))
print(vars(codigo2))
#print(codigo.limpar_numero('0710802-55.2018.8.02.0001'))