import re
class TratamentoDados:
  _REGEX_ASPAS_COLCHETE = r'^[\'"\[\]]|[\'"\[\]]$'
  _REGEX_SEPARAR_DATA = r'\d{2}[-\/]\d{2}[-\/]\d{4}'
  def remover_aspas(strings):
    for string in strings:
      return re.sub(TratamentoDados._REGEX_ASPAS_COLCHETE, '', string)
    
  def separar_string_por_data(string):
    return re.split(TratamentoDados._REGEX_SEPARAR_DATA, string)