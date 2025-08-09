from django.urls import path

from sigcontas.despesas.api.views import DespesaListCreateView
from .views import CriarDespesaView

urlpatterns = [
    path("create/", CriarDespesaView.as_view(), name="despesa-create"),
    path('despesas/', DespesaListCreateView.as_view(), name='despesa-list'),
    path('despesas/nova/', DespesaListCreateView.as_view(), name='despesa-create'),
]