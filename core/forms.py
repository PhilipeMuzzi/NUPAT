from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'profissao']


class RegistroUsuarioForm(forms.ModelForm):
    telefone = forms.CharField(max_length=15, required=True)
    endereco = forms.CharField(max_length=255, required=True)
    profissao = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'telefone', 'endereco', 'profissao']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()

            Perfil.objects.create(
                usuario=user,
                telefone=self.cleaned_data['telefone'],
                endereco=self.cleaned_data['endereco'],
                profissao=self.cleaned_data['profissao'],
                tipo_usuario='comum'
            )
        return user



