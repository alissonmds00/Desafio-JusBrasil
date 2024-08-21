from desafio.services.app import App
from desafio.models.processo import Processo
from desafio.utils.processos import NumeroProcesso
from desafio.utils.tratamento_dados import TratamentoDados as td
from django.db import transaction

class ConsultaService:
    def verificar_processo_db(self, processo):
        numero_processo_formatado = NumeroProcesso(processo).numero
        return Processo.objects.filter(numero_do_processo=numero_processo_formatado)

    def obter_numero_processo(self, request, numero_processo):
        if numero_processo:
            return numero_processo
        return request.query_params.get('numero_processo')

    def obter_dados_crawler(self, processo):
        return App(processo).iniciar_consulta()
    
    def get_first_non_null(self, data, keys, default=None):
        for key in keys:
            dado = data.get(key)
            if dado:
                return dado
        return default

    def salvar_processo_db(self, dados, numero_processo):
        numero_processo_formatado = NumeroProcesso(numero_processo).numero
        for grau, dado in enumerate(dados, start=1):
            print(dado)
            self.criar_processo(dado, numero_processo_formatado, grau)
            

    @transaction.atomic
    def criar_processo(self, dado, numero_processo_formatado, grau):
        try:
            Processo.objects.create(
                numero_do_processo=numero_processo_formatado,
                grau=grau,
                classe=td.remover_aspas(self.get_first_non_null(dado, ['classe'], '')),
                area=td.remover_aspas(self.get_first_non_null(dado, ['area'], '')),
                assunto=td.remover_aspas(self.get_first_non_null(dado, ['assunto'], '')),
                data_de_distribuicao=self.get_first_non_null(dado, ['data_de_distribuicao'], '1970-01-01'),
                juiz=td.remover_aspas(self.get_first_non_null(dado, ['juiz'], 'Desconhecido')),
                valor_da_acao=td.formatar_dinheiro_float(self.get_first_non_null(dado, ['valor_acao'], 0))
            )
        except Exception as e:
            transaction.set_rollback(True)
            raise e