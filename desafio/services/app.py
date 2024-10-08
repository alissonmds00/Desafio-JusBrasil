from desafio.utils.processos import NumeroProcesso
from desafio.utils.crawler import Crawler

class App:
  def __init__(self, numero_processo):
    self._urls = {
      'tjal': [
        'https://www2.tjal.jus.br/cpopg/open.do',
        'https://www2.tjal.jus.br/cposg5/open.do'
      ],
      'tjce': [
        'https://esaj.tjce.jus.br/cpopg/open.do',
        'https://esaj.tjce.jus.br/cposg5/open.do'
      ]
    }
    processo = NumeroProcesso(numero_processo)
    self._numero_processo = processo.numero_consulta
    self._uf_processo = self.verificar_uf_processo(processo.codigo_estado)
    self._respostas = []

  def verificar_uf_processo(self, codigo_uf):
    match codigo_uf:
      case '02':
        return 'tjal'
      case '06':
        return 'tjce'
      case _:
        raise ValueError('Estado não suportado')

  def consultar(self, tribunal):
    elementos = {
      'tjal': [
        ['classe', 'classeProcesso', 'ID'],
        ['area', 'areaProcesso', 'ID'],
        ['assunto', 'assuntoProcesso', 'ID'],
        ['juiz', 'juizProcesso', 'ID'],
        ['valor_acao', 'valorAcaoProcesso', 'ID'],
        ['partes', 'tablePartesPrincipais', 'ID'],
        ['partes_2', 'tableTodasPartes', 'ID'], 
        ['movimentacoes', 'fundoEscuro containerMovimentacao', 'CLASS_NAME'],
        ['movimentacoes_2', 'fundoClaro movimentacaoProcesso', 'CLASS_NAME']
      ],
      'tjce': [
        ['classe', 'classeProcesso', 'ID'],
        ['area', 'areaProcesso', 'ID'],
        ['assunto', 'assuntoProcesso', 'ID'],
        ['partes', 'tablePartesPrincipais', 'ID'],
        ['partes_2', 'tableTodasPartes', 'ID'], 
        ['movimentacoes', 'fundoEscuro containerMovimentacao', 'CLASS_NAME'],
        ['movimentacoes_2', 'fundoClaro movimentacaoProcesso', 'CLASS_NAME']
      ]
    }
    for url in self._urls[tribunal]:
      crawler = Crawler(url, 'numeroDigitoAnoUnificado', False)
      crawler.set_fields_target(elementos[tribunal])
      crawler.set_process_number(self._numero_processo)
      resultado = crawler.init()
      if not resultado:
        return None if not self._respostas else self._respostas
      self._respostas.append(resultado)
    return self._respostas

  def consultar_tjal(self):
    return self.consultar('tjal')

  def consultar_tjce(self):
    return self.consultar('tjce')
  
  def iniciar_consulta(self):
    if self._uf_processo == 'tjal':
      return self.consultar_tjal()
    return self.consultar_tjce()