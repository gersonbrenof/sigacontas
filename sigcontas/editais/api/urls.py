from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EditalViewSet, ConvenioViewSet

router = DefaultRouter()
router.register(r'editais', EditalViewSet, basename='edital')
router.register(r'convenios', ConvenioViewSet, basename='convenio')

urlpatterns = [
    path('api/', include(router.urls)),
]
