from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Projeto, DuvidaUsuario, PesquisaOpiniao


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'instituto', 'foto_perfil', 'nome_completo']

class PerfilAdminForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'endereco', 'instituto', 'foto_perfil', 'tipo_usuario', 'nome_completo']

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
    nome_completo = forms.CharField(max_length=150, required=True, label="Nome Completo")
    class Meta:
        model = User
        fields = ['username', 'email', 'nome_completo', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nome_completo']
        if commit:
            user.save()
        return user




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
