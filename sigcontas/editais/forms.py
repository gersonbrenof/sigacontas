from django import forms
from .models import Edital, Convenio

class EditalForm(forms.ModelForm):
    class Meta:
        model = Edital
        fields = ['numero', 'titulo', 'descricao', 'data_publicacao', 'data_limite_submissao', 'convenio', 'liberar_cadastro']

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = ['numero', 'nome', 'data_inicio', 'data_fim']
