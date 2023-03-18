from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filme'

    def ready(self):  # Para identificar o usuário e a senha do ADMIN no ambiente
        from .models import Usuario
        import os

        email = os.getenv("EMAIL_ADMIN")  # Crie seu email no ambiente
        senha = os.getenv("SENHA_ADMIN")  # Crie sua senha no ambiente

        usuarios = Usuario.objects.filter(email=email)
        if not usuarios:
            Usuario.objects.create_superuser(username="admin", email=email, password=senha, is_active=True, is_staff=True)
