from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from ..models import Despesa
from .serializers import DespesaSerializer

class DespesaViewSet(viewsets.ModelViewSet):
    serializer_class = DespesaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin vê todas as despesas
            return Despesa.objects.all()
        else:
            # Professor vê apenas suas próprias despesas
            return Despesa.objects.filter(professor=user)

    def perform_create(self, serializer):
        # Sempre vincula a despesa ao usuário logado
        serializer.save(professor=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Impede edição de despesas antigas
        if instance.data < date.today():
            return Response(
                {"error": "Despesas passadas não podem ser atualizadas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.data < date.today():
            return Response(
                {"error": "Despesas passadas não podem ser alteradas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)