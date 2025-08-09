from django.contrib import admin
from django.http import HttpResponse
import xlsxwriter
from reportlab.pdfgen import canvas
from .models import Despesa
import io

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'professor')  # <- Adicionamos 'professor' aqui
    search_fields = ('descricao', 'professor__username')        # <- Permite buscar por nome de usuário
    list_filter = ('data', 'professor')                         # <- Adicionamos filtro por professor
    actions = ['exportar_para_xlsx', 'exportar_para_pdf']

    def exportar_para_xlsx(self, request, queryset):
        """Gera e exporta um relatório XLSX com as despesas selecionadas."""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Escreve os cabeçalhos
        headers = ['Descrição', 'Valor', 'Data', 'Professor']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Escreve os dados
        for row_num, despesa in enumerate(queryset, start=1):
            worksheet.write(row_num, 0, despesa.descricao)
            worksheet.write(row_num, 1, str(despesa.valor))
            worksheet.write(row_num, 2, despesa.data.strftime('%d/%m/%Y'))
            worksheet.write(row_num, 3, despesa.professor.username if despesa.professor else '---')

        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=despesas.xlsx'
        return response

    exportar_para_xlsx.short_description = "Exportar para XLSX"

    def exportar_para_pdf(self, request, queryset):
        """Gera e exporta um relatório PDF com as despesas selecionadas."""
        output = io.BytesIO()
        p = canvas.Canvas(output)

        p.drawString(100, 800, "Relatório de Despesas")
        y = 780

        for despesa in queryset:
            linha = f"{despesa.descricao} - R$ {despesa.valor} - {despesa.data.strftime('%d/%m/%Y')} - {despesa.professor.username if despesa.professor else '---'}"
            p.drawString(100, y, linha)
            y -= 20

        p.save()
        output.seek(0)

        response = HttpResponse(output, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=despesas.pdf'
        return response

    exportar_para_pdf.short_description = "Exportar para PDF"