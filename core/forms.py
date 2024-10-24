from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Projeto, DuvidaUsuario, PesquisaOpiniao


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'instituto', 'foto_perfil']  # Sem tipo_usuario para usuários normais

class PerfilAdminForm(forms.ModelForm):  # Form para admin editar tipo de usuário
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'instituto', 'foto_perfil', 'tipo_usuario']  # Inclui o tipo de usuário

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo_usuario']


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'resumo', 'resultados', 'fotos', 'situacao', 'descricao', 'artigos', 'pesquisadores', 'instituicoes', 'alunos']

class RegistroUsuarioForm(UserCreationForm):
    telefone = forms.CharField(max_length=15, required=True)
    endereco = forms.CharField(max_length=255, required=True)
    instituto = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DuvidaForm(forms.ModelForm):
    class Meta:
        model = DuvidaUsuario
        fields = ['mensagem']



class PesquisaOpiniaoForm(forms.ModelForm):
    class Meta:
        model = PesquisaOpiniao
        fields = ['nota']

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
