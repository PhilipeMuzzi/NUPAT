from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Projeto


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'instituto', 'foto_perfil']


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'resumo', 'resultados', 'fotos', 'situacao', 'descricao', 'artigos', 'pesquisadores', 'instituicoes', 'alunos']  # Adicione todos os campos que você deseja editar

class RegistroUsuarioForm(UserCreationForm):
    telefone = forms.CharField(max_length=15, required=True)
    endereco = forms.CharField(max_length=255, required=True)
    instituto = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()

            # Criando o perfil com valores do formulário
            Perfil.objects.create(
                usuario=user,
                telefone=self.cleaned_data['telefone'],
                endereco=self.cleaned_data['endereco'],
                instituto=self.cleaned_data['instituto'],
                perfil='Aluno'
            )
        return user


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()

            Perfil.objects.create(
                usuario=user,
                telefone=self.cleaned_data['telefone'],
                endereco=self.cleaned_data['endereco'],
                instituto=self.cleaned_data['instituto'],
                tipo_usuario=''  #deixando vazio até que o admin de fato defina
            )
        return user
