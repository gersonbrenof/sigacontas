from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sigcontas.users.api.views import UserViewSet, CustomLoginView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path("users/", include("sigcontas.users.api.urls")),
    path("login/", CustomLoginView.as_view(), name="custom_login"),
    path("", include(router.urls)),
]
