from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DespesaViewSet

# Criar roteador para as rotas da API
router = DefaultRouter()
router.register(r'despesas', DespesaViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclui todas as rotas do router

]