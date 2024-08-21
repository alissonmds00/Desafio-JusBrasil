import re
class TratamentoDados:
  _REGEX_ASPAS_COLCHETE = r'^[\'"\[\]]|[\'"\[\]]$'
  _REGEX_SEPARAR_DATA = r'\d{2}[-\/]\d{2}[-\/]\d{4}'
  _REGEX_DINHEIRO_FLOAT = r'[^0-9.,]'
  def remover_aspas(strings):
    for string in strings:
      return re.sub(TratamentoDados._REGEX_ASPAS_COLCHETE, '', string)
    
  def separar_string_por_data(string):
    return re.split(TratamentoDados._REGEX_SEPARAR_DATA, string)
  
  def limpar_caracteres(string):
    string = re.sub(r'\s+', ' ', string)
    return string.strip()
  
  def formatar_dinheiro_float(valor):
        valor = TratamentoDados.remover_aspas(valor)
        valor = re.sub(r'[^\d,]', '', valor).replace('.', '').replace(',', '.')
        return float(valor)
  