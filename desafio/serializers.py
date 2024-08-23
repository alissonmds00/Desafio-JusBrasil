from rest_framework import serializers
from desafio.models.processo import Processo
from desafio.utils.tratamento_dados import TratamentoDados as td

class ProcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processo
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        #Transformar partes e 'movimentações' de string para array
        if 'partes' in representation:
            representation['partes'] = td.formatar_dados_partes(representation['partes'])
        if 'movimentacoes' in representation:
            representation['movimentacoes'] = td.formatar_dados_movimentacoes(representation['movimentacoes'])
        return representation
    