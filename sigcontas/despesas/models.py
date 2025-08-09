from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Despesa(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="despesas"
    )

    def __str__(self):

        return self.descricao