from django.urls import path
from rest_framework.generics import ListAPIView
from .models import User
from sigcontas.users.serializers import UserSerializer
from .views import (
    RegisterView, LoginView, ProtectedView,
    user_detail_view, user_redirect_view, user_update_view,
    user_pdf_report_view, user_xlsx_report_view
)

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("~redirect/", user_redirect_view, name="redirect"),
    path("~update/", user_update_view, name="update"),
    path("<str:username>/", user_detail_view, name="detail"),
    
    path("export/pdf/", user_pdf_report_view, name="user-export-pdf"),
    path("export/xlsx/", user_xlsx_report_view, name="user-export-xlsx"),
]