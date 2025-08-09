from rest_framework import viewsets, permissions, filters
from editais.models import Edital, Convenio
from .serializers import EditalSerializer, ConvenioSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ConvenioViewSet(viewsets.ModelViewSet):
    queryset = Convenio.objects.all()
    serializer_class = ConvenioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['numero']
    search_fields = ['numero']
    ordering_fields = ['data_inicio', 'data_fim']

class EditalViewSet(viewsets.ModelViewSet):
    queryset = Edital.objects.all()
    serializer_class = EditalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['numero', 'convenio']
    search_fields = ['numero', 'titulo']
    ordering_fields = ['data_publicacao', 'data_limite_submissao']
