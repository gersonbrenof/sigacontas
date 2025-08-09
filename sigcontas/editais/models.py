from django.db import models


class Convenio(models.Model):
    nome = models.CharField("Nome do Convênio", max_length=255)
    numero = models.CharField("Número", max_length=100, unique=True)
    data_inicio = models.DateField("Data de Início")
    data_fim = models.DateField("Data de Término", null=True, blank=True)

    def __str__(self):
        return f"{self.numero} - {self.nome}"

class Edital(models.Model):
    numero = models.CharField("Número do Edital", max_length=100, unique=True)
    titulo = models.CharField("Título", max_length=255)
    descricao = models.TextField("Descrição", blank=True)
    data_publicacao = models.DateField("Data de Publicação")
    data_limite_submissao = models.DateField("Data Limite para Submissão")
    convenio = models.ForeignKey('Convenio', on_delete=models.CASCADE, verbose_name="Convênio", null=True, blank=True)
    liberar_cadastro = models.BooleanField("Liberar Cadastro de Projetos", default=False)


    def __str__(self):
        return f"{self.numero} - {self.titulo}"
