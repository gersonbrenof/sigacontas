from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from sigcontas.users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.http import JsonResponse


# View para registrar usuários
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        is_professor = request.data.get("is_professor", False)

        if not username or not password:
            return Response({"error": "Usuário e senha são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, is_professor=is_professor)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Usuário criado com sucesso!",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# View para gerar tokens JWT (Login)
class LoginView(APIView):
    permission_classes = [AllowAny]  # Permite qualquer usuário acessar

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

# View protegida para testar autenticação
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Exige autenticação

    def get(self, request):
        return Response({"message": f"Bem-vindo, {request.user.username}!"})

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        # Redireciona o usuário para sua própria página de detalhes
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

import io
import xlsxwriter  # Biblioteca para criar arquivos Excel
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from reportlab.pdfgen import canvas  # Biblioteca para criar PDFs
from django.views import View

from sigcontas.users.models import User


class UserPDFReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Configura a resposta HTTP para um arquivo PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="user_report.pdf"'

        # Cria um buffer de memória para armazenar o PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)

        # Obtém todos os usuários do sistema
        users = User.objects.all()
        y_position = 800  # Posição inicial no PDF

        # Adiciona título ao relatório
        p.drawString(100, y_position, "Relatório de Usuários")
        y_position -= 40  # Move para a próxima linha

        # Escreve os dados dos usuários no PDF
        for user in users:
            p.drawString(100, y_position, f"ID: {user.id} | Nome: {user.name} | Username: {user.username}")
            y_position -= 20  # Move para a próxima linha

        # Finaliza o documento e salva no buffer
        p.showPage()
        p.save()

        # Retorna o arquivo PDF gerado
        buffer.seek(0)
        response.write(buffer.getvalue())
        return response
    
    
class UserXLSXReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Cria um buffer de memória para armazenar o arquivo XLSX
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Obtém todos os usuários do sistema
        users = User.objects.all()

        # Define os cabeçalhos das colunas
        headers = ["ID", "Nome", "Username"]
        worksheet.write_row(0, 0, headers)  # Escreve a linha de cabeçalhos na primeira linha

        # Escreve os dados dos usuários no arquivo XLSX
        row = 1
        for user in users:
            worksheet.write(row, 0, user.id)
            worksheet.write(row, 1, user.name)
            worksheet.write(row, 2, user.username)
            row += 1  # Avança para a próxima linha

        # Fecha o workbook e move o buffer para o início
        workbook.close()
        output.seek(0)

        # Configura a resposta HTTP para um arquivo XLSX
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="user_report.xlsx"'
        return response


# Criação das instâncias das views para exportação
user_pdf_report_view = UserPDFReportView.as_view()
user_xlsx_report_view = UserXLSXReportView.as_view()

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from django.http import JsonResponse

class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            return JsonResponse({
                "access": response.data["access"],
                "refresh": response.data["refresh"],
                "redirect_url": "/despesas/create/"
            })

        return response