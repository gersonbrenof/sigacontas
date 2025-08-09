from rest_framework import serializers
from despesas.models import Despesa  # Certifique-se de que o modelo existe

class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = "__all__"
        read_only_fields = ("professor",)