from rest_framework import serializers
from editais.models import Edital, Convenio

class ConvenioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convenio
        fields = '__all__'

class EditalSerializer(serializers.ModelSerializer):
    convenio = ConvenioSerializer(read_only=True)  # Para leitura do convênio já existente
    convenio_id = serializers.PrimaryKeyRelatedField(
        queryset=Convenio.objects.all(), source='convenio', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Edital
        fields = ['id', 'numero', 'titulo', 'descricao', 'data_publicacao', 'data_limite_submissao', 'convenio', 'convenio_id']

    def create(self, validated_data):
        convenio_data = validated_data.pop('convenio', None)
        convenio_id = validated_data.pop('convenio_id', None)

        if convenio_id:  # Se o ID do convênio for passado, usamos ele
            convenio = Convenio.objects.get(id=convenio_id)
        elif convenio_data:  # Caso contrário, tentamos criar um novo convênio
            convenio = Convenio.objects.create(**convenio_data)
        else:
            convenio = None

        edital = Edital.objects.create(convenio=convenio, **validated_data)
        return edital
