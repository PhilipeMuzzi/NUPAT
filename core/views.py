from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse

from .forms import RegistroUsuarioForm, PerfilForm
from .models import Perfil, Projeto, Pesquisador, Parceiro, Instituicao
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

# view para  editar usuários pelo admin (staff)
@staff_member_required
def editar_tipo_usuario(request, usuario_id):
    perfil = get_object_or_404(Perfil, user_id=usuario_id)
    if request.method == 'POST':
        novo_tipo = request.POST.get('tipo_usuario')
        perfil.tipo_usuario = novo_tipo
        perfil.save()
        messages.success(request, 'Tipo de usuário atualizado com sucesso.')
        return redirect('detalhes_usuario', usuario_id=usuario_id)
    return render(request, 'admin/editar_tipo_usuario.html', {'perfil': perfil})



def inicio(request):
    # traz os 6 últimos projetos mais recentes para a primeira seção
    ultimos_projetos = Projeto.objects.order_by('-id')[:6]

    return render(request, 'index.html', {
        'ultimos_projetos': ultimos_projetos
    })


def quem_somos(request):
    return render(request, 'Quem Somos/quem_somos.html')

def area_suporte(request):
    return render(request, 'Área de Suporte/area_suporte.html')


def atendimento_virtual(request):
    return render(request, 'Atendimento virtual/atendimento_virtual.html')




# view para registro de novos usuários

def registro(request):
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('login')  # redirecionando para a página de login
    else:
        formulario = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'formulario': formulario})


def atualiza_perfil(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario_id=usuario_id)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('detalhes_usuario', usuario_id=usuario_id)  # Redireciona após salvar
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'usuarios/editardetalhes.html', {'form': form, 'perfil': perfil})
# views.py
def detalhes_usuario(request, usuario_id):
    print(f"Usuario ID: {usuario_id}")
    try:
        perfil = Perfil.objects.get(usuario__id=usuario_id)
        print(f"Perfil encontrado: {perfil}")
    except Perfil.DoesNotExist:
        print("Perfil não encontrado")
        return render(request, '404.html')

    return render(request, 'usuarios/detalhes_usuario.html', {'perfil': perfil})


def editar_detalhes(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario__id=usuario_id)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'As informações foram atualizadas com sucesso!')
            return redirect('detalhes_usuario', usuario_id=usuario_id)
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'usuarios/editardetalhes.html', {'form': form, 'perfil': perfil})
# Login
@login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Verifica se o usuário é superuser ou staff (admin)
            if user.is_superuser or user.is_staff:
                # Redireciona para o dashboard de admin
                return redirect('admin_dashboard')
            else:
                # Redireciona para a página de usuário comum
                return redirect('index')
        else:
            # Caso as credenciais estejam incorretas
            messages.error(request, 'Credenciais inválidas.')
            return render(request, 'login.html')

    return render(request, 'login.html')


# verificando se é administrador
def admin_check(user):
    return user.is_staff or user.is_superuser

@staff_member_required
def admin_dashboard(request):
    # lógica do dashboard
    return render(request, 'admin/dashboard.html')

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('admin_dashboard')  # envia administradores para o painel de administração html (dashboard)
        return reverse('inicio')  # envia usuários comuns para a página inicial do site


# função para verificar se o usuário é admin (is_staff)
def is_admin(user):
    return user.is_staff

# view que controla a rota apenas admins (é o que é mostrado se entrar como admin do terminal)
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin/dashboardAdmin.html')

# Listagem de projetos

def listar_projetos(request):
    pesquisa= request.GET.get('pesquisa')
    print(pesquisa)

    if pesquisa:
        projetos = Projeto.objects.filter(titulo__icontains=pesquisa)
    else:
        projetos = Projeto.objects.all()
    
    return render(request, 'projetos/lista_projetos.html', {'projetos': projetos})

# view para ver detalhes de um projeto

def detalhes_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    alunos = projeto.alunos.all()
    parceiros = projeto.pesquisadores.all()
    return render(request, 'projetos/detalhes_projeto.html', {
        'projeto': projeto,
        'alunos': alunos,
        'parceiros': parceiros
    })

# Adicionar um novo projeto (Apenas o admin pode acessar)
@staff_member_required
def adicionar_projeto(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        resumo = request.POST.get('resumo')
        resultados = request.POST.get('resultados')
        situacao = request.POST.get('situacao')
        descricao = request.POST.get('descricao')

        # Obtendo arquivos, se houver
        fotos = request.FILES.get('fotos', None)
        artigos = request.FILES.get('artigos', None)

        # Criação do objeto projeto
        projeto = Projeto.objects.create(
            titulo=titulo,
            resumo=resumo,
            resultados=resultados,
            situacao=situacao,
            descricao=descricao,
            fotos=fotos,
            artigos=artigos
        )


        pesquisadores = request.POST.getlist('pesquisadores')
        for pesquisador_id in pesquisadores:
            pesquisador = Pesquisador.objects.get(id=pesquisador_id)
            projeto.pesquisadores.add(pesquisador)


        instituicoes = request.POST.getlist('instituicoes')
        for instituicao_id in instituicoes:
            instituicao = Instituicao.objects.get(id=instituicao_id)
            projeto.instituicoes.add(instituicao)

        projeto.save()

        messages.success(request, 'Projeto cadastrado com sucesso.')
        return redirect('listar_projetos')


    pesquisadores = Pesquisador.objects.all()
    instituicoes = Instituicao.objects.all()

    return render(request, 'projetos/adicionar_projeto.html', {
        'pesquisadores': pesquisadores,
        'instituicoes': instituicoes
    })

# View para admin editar um projeto
@login_required
def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        projeto.titulo = request.POST.get('titulo')
        projeto.resumo = request.POST.get('resumo')
        projeto.resultados = request.POST.get('resultados')
        projeto.situacao = request.POST.get('situacao')
        projeto.descricao = request.POST.get('descricao')
        if request.FILES.get('fotos'):
            projeto.fotos = request.FILES.get('fotos')
        if request.FILES.get('artigos'):
            projeto.artigos = request.FILES.get('artigos')
        projeto.pesquisadores.clear()
        projeto.instituicoes.clear()
        pesquisadores = request.POST.getlist('pesquisadores')
        for pesquisador_id in pesquisadores:
            projeto.pesquisadores.add(Pesquisador.objects.get(id=pesquisador_id))
        instituicoes = request.POST.getlist('instituicoes')
        for instituicao_id in instituicoes:
            projeto.instituicoes.add(Instituicao.objects.get(id=instituicao_id))
        projeto.save()
        messages.success(request, 'Projeto atualizado com sucesso.')
        return redirect('listar_projetos')
    pesquisadores = Pesquisador.objects.all()
    instituicoes = Instituicao.objects.all()
    return render(request, 'projetos/editar_projeto.html', {'projeto': projeto, 'pesquisadores': pesquisadores, 'instituicoes': instituicoes})

# view para deletar o projeto
@login_required
def deletar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        projeto.delete()
        messages.success(request, 'Projeto deletado com sucesso.')
        return redirect('listar_projetos')
    return render(request, 'projetos/deletar_projeto.html', {'projeto': projeto})




# listagem de pesquisadores
@login_required
def listar_pesquisadores(request):
    pesquisadores = Pesquisador.objects.all()
    return render(request, 'pesquisadores/lista_pesquisadores.html', {'pesquisadores': pesquisadores})


# adicionar novo pesquisador
@login_required
def adicionar_pesquisador(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        perfil = Pesquisador.objects.create(nome=nome, email=email)
        messages.success(request, 'Pesquisador adicionado com sucesso.')
        return redirect('listar_pesquisadores')
    return render(request, 'pesquisadores/adicionar_pesquisador.html')


def save(self, commit=True):
    user = super().save(commit=False)
    if commit:
        user.save()
        tipo_usuario = self.cleaned_data.get('tipo_usuario')

        if tipo_usuario == 'pesquisador':
            # Criar ou associar o perfil de pesquisador, por exemplo:
            Pesquisador.objects.create(user=user, contato=self.cleaned_data.get('telefone'))
        else:
            Perfil.objects.create(
                user=user,
                telefone=self.cleaned_data.get('telefone'),
                endereco=self.cleaned_data.get('endereco'),
                profissao=self.cleaned_data.get('profissao'),
                tipo_usuario=tipo_usuario,
            )
    return user


# parceiros
@login_required
def listar_parceiros(request):
    parceiros = Parceiro.objects.all()
    return render(request, 'parceiros/lista_parceiros.html', {'parceiros': parceiros})


# Adicionar novo parceiro
@login_required
def adicionar_parceiro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        parceiro = Parceiro.objects.create(nome=nome, email=email)
        messages.success(request, 'Parceiro adicionado com sucesso.')
        return redirect('listar_parceiros')
    return render(request, 'parceiros/adicionar_parceiro.html')

# Listagem de instituições
@login_required
def listar_instituicoes(request):
    instituicoes = Instituicao.objects.all()
    return render(request, 'instituicoes/lista_instituicoes.html', {'instituicoes': instituicoes})

# Adicionar nova instituição
@login_required
def adicionar_instituicao(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        instituicao = Instituicao.objects.create(nome=nome, endereco=endereco)
        messages.success(request, 'Instituição adicionada com sucesso.')
        return redirect('listar_instituicoes')
    return render(request, 'instituicoes/adicionar_instituicao.html')



#listagem de usuários
@login_required
def lista_usuarios(request):
    # listar os usuários e seus perfis
    usuarios = Perfil.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def detalhes_usuario(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario_id=usuario_id)

    return render(request, 'usuarios/detalhes_usuario.html', {'perfil': perfil})
