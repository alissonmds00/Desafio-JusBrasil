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
    processo = self._obter_numero_processo(request, numero_processo)
    if not processo:
      return Response({'message': 'Número do processo não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    #Consulta e verifica se o processo está no banco de dados
    processo_db = self._verificar_processo_db(processo)
    if processo_db.exists():
      return Response(list(processo_db.values()), status=status.HTTP_200_OK)
    
    #Utiliza o crawler para obter os dados do processo
    resultado_crawler = self._obter_dados_crawler(processo)
    if not resultado_crawler:
      return Response({'message': 'Processo não encontrado'}, status=status.HTTP_404_NOT_FOUND) 
    
    #Salva os dados do processo no banco de dados
    self._salvar_processo_db(resultado_crawler, processo)
    processo_db = self._verificar_processo_db(processo)
    return Response(list(processo_db.values()), status=status.HTTP_201_CREATED)
  
  
  def _verificar_processo_db(self, processo):
    """
    Verifica se o processo já existe no banco de dados.
    """
    numero_processo_formatado = NumeroProcesso(processo).numero
    return Processo.objects.filter(numero_do_processo=numero_processo_formatado)
  
  def _obter_numero_processo(self, request, numero_processo):
    if numero_processo:
      return numero_processo
    return request.query_params.get('numero_processo')
  
  def _obter_dados_crawler(self, processo):
    """
    Inicia o crawler para obter os dados do processo.
    """
    return App(processo).iniciar_consulta()

  def _salvar_processo_db(self, dados, numero_processo):
    """
    Envia os dados para a criação do processo posteriormente
    """
    numero_processo_formatado = NumeroProcesso(numero_processo).numero
    for grau, dado in enumerate(dados, start=1):
      self._criar_processo(dado, numero_processo_formatado, grau)
  
  @transaction.atomic
  def _criar_processo(self, dado, numero_processo_formatado, grau):
    """
    Cria um objeto processo que será persistido no banco de dados
    """
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
    
  
    
