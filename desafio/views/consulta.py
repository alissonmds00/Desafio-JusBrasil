from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from desafio.services.consulta_service import ConsultaService

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
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.consulta_service = ConsultaService()

  def get(self, request, numero_processo=None):
      # Verifica se o número de processo foi fornecido
      processo = self.consulta_service.obter_numero_processo(request, numero_processo)
      if not processo:
          return Response({'message': 'Número do processo não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

      # Consulta e verifica se o processo está no banco de dados
      processo_db = self.consulta_service.verificar_processo_db(processo)
      if processo_db:
          return Response(processo_db, status=status.HTTP_200_OK)

      # Utiliza o crawler para obter os dados do processo
      resultado_crawler = self.consulta_service.obter_dados_crawler(processo)
      if not resultado_crawler:
          return Response({'message': 'Processo não encontrado'}, status=status.HTTP_404_NOT_FOUND)

      # Salva os dados do processo no banco de dados
      self.consulta_service.salvar_processo_db(resultado_crawler, processo)
      processo_db = self.consulta_service.verificar_processo_db(processo)
      return Response(processo_db, status=status.HTTP_201_CREATED)