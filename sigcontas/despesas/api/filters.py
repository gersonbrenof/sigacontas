import django_filters
from despesas.models import Despesa

class DespesaFilter(django_filters.FilterSet):
    min_valor = django_filters.NumberFilter(field_name="valor", lookup_expr='gte')  # Maior ou igual
    max_valor = django_filters.NumberFilter(field_name="valor", lookup_expr='lte')  # Menor ou igual
    data = django_filters.DateFilter(field_name="data")  # Filtrar por data exata
    descricao = django_filters.CharFilter(field_name="descricao", lookup_expr='icontains')  # Busca parcial

    class Meta:
        model = Despesa
        fields = ['min_valor', 'max_valor', 'data', 'descricao']