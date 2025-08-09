from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models 
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Modelo de usuário personalizado para o sigcontas.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    is_professor = models.BooleanField(default=False, help_text="Indica se o usuário é um professor")

    def get_absolute_url(self) -> str:
        """Retorna a URL do perfil do usuário."""
        return reverse("users:detail", kwargs={"username": self.username})

    def set_unusable_password(self):
        """Define uma senha inutilizável para o usuário."""
        self.password = "!"

    def has_usable_password(self):
        """Verifica se o usuário tem uma senha utilizável."""

        return self.password and not self.password.startswith("!")
