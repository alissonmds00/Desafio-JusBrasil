import re

class NumeroProcesso:
  REGEX_FORMATAR = re.compile(r"(\d{7})(\d{2})(\d{4})(\d)(\d{2})(\d{4})")
  REGEX_OBTER_ESTADO = re.compile(r'^\d{7}-\d{2}\.\d{4}\.\d\.(\d{2})\.\d{4}$')
  REGEX_OBTER_NUMERO_SEM_CODIGO_REGIAO = re.compile(r'^(\d{7}-\d{2}\.\d{4}\.)\d\.\d{2}\.(\d{4})$')

  def __init__(self, numero):
    if len(numero) < 20:
      raise ValueError('Código inválido')
    numero_processo = self._validar_numero(numero)
    if numero_processo:
      self._numero = numero_processo
      self._codigo_estado = self._obter_estado(numero_processo)
      self._numero_consulta = self._obter_numero_sem_codigo_regiao(numero_processo)

  @property
  def numero(self):
    return self._numero

  @property
  def codigo_estado(self):
    return self._codigo_estado
      
  @property
  def numero_consulta(self):
    return self._numero_consulta

  def _limpar_numero(self, numero):
    return re.sub(r'\D', '', numero)

  def _formatar_numero(self, numero):
    if len(numero) != 20 or not numero.isdigit():
      raise ValueError("O número deve ter exatamente 20 dígitos.")
    return self.REGEX_FORMATAR.sub(r"\1-\2.\3.\4.\5.\6", numero)

  def _validar_numero(self, numero):
    numero_limpo = self._limpar_numero(numero)
    return self._formatar_numero(numero_limpo)

  def _obter_estado(self, codigo):
    match = self.REGEX_OBTER_ESTADO.search(codigo)
    return match.group(1) if match else None

  def _obter_numero_sem_codigo_regiao(self, codigo):
    match = self.REGEX_OBTER_NUMERO_SEM_CODIGO_REGIAO.search(codigo)
    if match:
      return f"{self._limpar_numero(match.group(1))}{self._limpar_numero(match.group(2))}"
    raise ValueError("Código inválido")