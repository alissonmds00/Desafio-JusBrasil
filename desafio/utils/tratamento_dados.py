import re
class TratamentoDados:
  _REGEX_ASPAS_COLCHETE = r'^[\'"\[\]]|[\'"\[\]]$'
  _REGEX_SEPARAR_DATA = r'\d{2}[-\/]\d{2}[-\/]\d{4}'
  _REGEX_DINHEIRO_FLOAT = r'[^0-9.,]'
  @staticmethod
  def remover_aspas(strings):
    for string in strings:
      return re.sub(TratamentoDados._REGEX_ASPAS_COLCHETE, '', string)
    
  @staticmethod
  def remover_aspas_mult_args(*args):
      for arg in args:
          if isinstance(arg, str) and arg:
              return arg.replace('"', '').replace("'", '')
      return ''
    
  @staticmethod
  def separar_string_por_data(string):
    return re.split(TratamentoDados._REGEX_SEPARAR_DATA, string)
  
  @staticmethod
  def limpar_caracteres(string):
    string = re.sub(r'\s+', ' ', string)
    return string.strip()
  
  @staticmethod
  def formatar_dinheiro_float(valor):
    try:
        valor = TratamentoDados.remover_aspas(valor)
        valor = re.sub(r'[^\d,]', '', valor).replace('.', '').replace(',', '.')
        return float(valor)
    except:
      return 0
  