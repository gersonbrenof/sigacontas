from django.contrib import admin, messages
from editais.models import Edital, Convenio
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from .forms import EditalForm

User = get_user_model()

@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ["numero", "nome", "data_inicio", "data_fim"]
    search_fields = ["numero", "nome"]
    list_filter = ["data_inicio", "data_fim"]

@admin.register(Edital)
class EditalAdmin(admin.ModelAdmin):
    form = EditalForm  # Usando o formulário customizado

    list_display = (
        "numero_link", "titulo", "data_publicacao",
        "data_limite_submissao", "convenio", "liberar_cadastro"
    )
    search_fields = ("numero", "titulo")
    list_filter = ("data_publicacao", "convenio__numero", "liberar_cadastro")

    fieldsets = (
        (_("Informações do Edital"), {
            "fields": (
                "numero", "titulo", "descricao",
                "data_publicacao", "data_limite_submissao",
                "convenio", "liberar_cadastro"
            )
        }),
    )

    actions = ["notificar_pesquisadores"]

    def numero_link(self, obj):
        url = reverse("admin:editais_edital_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.numero)

    def notificar_pesquisadores(self, request, queryset):
        pesquisadores = User.objects.filter(groups__name="Pesquisadores")

        if not pesquisadores.exists():
            self.message_user(request, "Nenhum pesquisador encontrado para notificação.", level=messages.WARNING)
            return

        emails = pesquisadores.exclude(email__isnull=True, email__exact='').values_list("email", flat=True)
        mensagens = []

        for edital in queryset:
            if not edital.liberar_cadastro:
                continue  # Só notifica se estiver liberado

            assunto = f"[SIGContas] Novo Edital Liberado: {edital.numero}"
            mensagem = (
                f"Olá!\n\nO edital \"{edital.titulo}\" está com o cadastro de projetos liberado.\n\n"
                f"Número do edital: {edital.numero}\n"
                f"Data de publicação: {edital.data_publicacao.strftime('%d/%m/%Y')}\n"
                f"Data limite de submissão: {edital.data_limite_submissao.strftime('%d/%m/%Y')}\n"
                f"Acesse o sistema para submeter seu projeto.\n"
            )

            for email in emails:
                mensagens.append((assunto, mensagem, "nao-responder@seudominio.com", [email]))

        if mensagens:
            send_mass_mail(mensagens, fail_silently=False)
            self.message_user(request, f"{len(emails)} pesquisadores foram notificados.", level=messages.SUCCESS)
        else:
            self.message_user(request, "Nenhum edital com cadastro liberado foi selecionado.", level=messages.WARNING)

    notificar_pesquisadores.short_description = "Notificar pesquisadores por e-mail"
