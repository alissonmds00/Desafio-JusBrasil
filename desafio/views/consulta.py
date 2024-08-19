from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from desafio.utils.app import App
from desafio.models.processo import Processo
from desafio.utils.processos import NumeroProcesso
from django.db import transaction

class ConsultaView(APIView):
  """
    Consulta um processo no banco de dados ou inicia o crawling para obter os dados do processo.

    Args:
      request: A requisição HTTP.
      numero_processo: O número do processo.

    Returns:
      Uma resposta HTTP com o objeto Processo caso ele já exista no banco de dados,
      ou com o resultado do crawler caso o processo não exista no banco de dados.
  """
  def get(self, request, numero_processo=None):
    #Verifica se o número de processo foi fornecido
    if numero_processo:
      processo = numero_processo
    elif 'processo' in request.query_params:
      processo = request.query_params['processo']
    else:
      return Response({'message': 'Número do processo não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    #Consulta e verifica se o processo está no banco de dados
    processo_db = self._verificar_processo_db(processo)
    
    if processo_db.exists():
      return Response(list(processo_db.values()), status=status.HTTP_200_OK)
    
    #Utiliza o crawler para obter os dados do processo
    resultado_crawler = App(processo).iniciar_consulta()
    if not resultado_crawler:
      return Response({'message': 'Processo não encontrado'}, status=status.HTTP_404_NOT_FOUND) 
    
    #Salva os dados do processo no banco de dados
    self.salvar_processo_no_banco(resultado_crawler, processo)
    
    #Consulta outra vez para retornar os processos salvos no banco de dado
    processo_db = self._verificar_processo_db(processo)
    return Response(list(processo_db.values()), status=status.HTTP_201_CREATED)
  
  def _verificar_processo_db(self, processo):
    """
    Verifica se o processo já existe no banco de dados.
    """
    processo_formatado = NumeroProcesso(processo).numero
    processo_db = Processo.objects.filter(numero_do_processo=processo_formatado)
    print(processo_formatado)
    return processo_db

  
  @transaction.atomic
  def salvar_processo_no_banco(self, dados, numero_do_processo):
    numero_processo_formatado = NumeroProcesso(numero_do_processo).numero
    grau = 0
    for dado in dados:
      grau += 1
      try:
        Processo.objects.create(
          numero_do_processo=numero_processo_formatado,
          grau=grau,
          classe=dado.get('classe', ''),
          area=dado.get('area', ''),
          assunto=dado.get('assunto', ''),
          data_de_distribuicao=dado.get('data_de_distribuicao', '1970-01-01'),
          juiz=dado.get('juiz', 'Desconhecido'),
          valor_da_acao=float(dado.get('valor_da_acao', 0))
        )
      except Exception as e:
        transaction.set_rollback(True)
        raise e
    
  
    
