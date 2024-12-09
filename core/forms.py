from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Projeto, DuvidaUsuario, PesquisaOpiniao, Pesquisador, Instituicao


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'instituto', 'foto_perfil']

class PerfilAdminForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'instituto', 'foto_perfil', 'tipo_usuario']

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo_usuario']


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'resumo', 'descricao', 'resultados', 'fotos', 'situacao', 'artigos', 'professores', 'pesquisadores', 'alunos', 'instituicoes']

    professores = forms.ModelMultipleChoiceField(
        queryset=Perfil.objects.filter(tipo_usuario='Professor'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    pesquisadores = forms.ModelMultipleChoiceField(
        queryset=Perfil.objects.filter(tipo_usuario='Pesquisador'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    alunos = forms.ModelMultipleChoiceField(
        queryset=Perfil.objects.filter(tipo_usuario='Aluno'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class RegistroUsuarioForm(UserCreationForm):
    telefone = forms.CharField(max_length=15, required=True)
    endereco = forms.CharField(max_length=255, required=True)
    instituto = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'instituto', 'telefone', 'endereco']

    def save(self, commit=True):
        user = super().save(commit=commit)



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
                tipo_usuario=''
            )
        return user
