from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


# Form de criação do usuário
class CriarContaForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')


class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)

    class Meta:
        model = Usuario
        fields = ('email')
