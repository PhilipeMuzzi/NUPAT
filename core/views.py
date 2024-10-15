from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistroUsuarioForm
from .models import Perfil, Projeto, Pesquisador, Parceiro, Instituicao
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required


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


# Página inicial


def inicio(request):
    return render(request, 'index.html')

# Novos usuários
def registro(request):
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            messages.success(request, 'Registro bem-sucedido! Bem-vindo, {}.'.format(usuario.username))
            return redirect('inicio')
    else:
        formulario = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'formulario': formulario})

# Login
@login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Verifica se o usuário é staff (admin)
            if user.is_staff:
                # Redireciona para o dashboard de admin
                return redirect('admin_dashboard')
            else:
                # Redireciona para a página de usuário comum
                return redirect('index')
        else:
            # Caso as credenciais estejam incorretas
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})

    return render(request, 'login.html')


# Função para verificar se o usuário é admin (is_staff)
def is_admin(user):
    return user.is_staff

# View protegida para apenas admins
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin/dashboardAdmin.html')

# Listagem de projetos

def listar_projetos(request):
    projetos = Projeto.objects.all()
    return render(request, 'projetos/lista_projetos.html', {'projetos': projetos})

# Detalhes de um projeto
@login_required
def detalhes_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    alunos = projeto.alunos.all()  # Assumindo que há uma relação ManyToMany com Alunos
    parceiros = projeto.parceiros.all()  # Assumindo que há uma relação ManyToMany com Parceiros
    return render(request, 'projetos/detalhes_projeto.html', {'projeto': projeto, 'alunos': alunos, 'parceiros': parceiros})

# Adicionar um novo projeto (Apenas o admin pode acessar)
@staff_member_required
def adicionar_projeto(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        resumo = request.POST.get('resumo')
        resultados = request.POST.get('resultados')
        situacao = request.POST.get('situacao')
        descricao = request.POST.get('descricao')

        # Verifica se há arquivos sendo enviados
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

        # Adiciona os pesquisadores ao projeto
        pesquisadores = request.POST.getlist('pesquisadores')
        for pesquisador_id in pesquisadores:
            pesquisador = Pesquisador.objects.get(id=pesquisador_id)
            projeto.pesquisadores.add(pesquisador)

        # Adiciona as instituições ao projeto
        instituicoes = request.POST.getlist('instituicoes')
        for instituicao_id in instituicoes:
            instituicao = Instituicao.objects.get(id=instituicao_id)
            projeto.instituicoes.add(instituicao)

        # Salva o projeto com todas as relações
        projeto.save()

        messages.success(request, 'Projeto cadastrado com sucesso.')
        return redirect('listar_projetos')

    # Carrega pesquisadores e instituições para o formulário
    pesquisadores = Pesquisador.objects.all()
    instituicoes = Instituicao.objects.all()

    return render(request, 'projetos/adicionar_projeto.html', {
        'pesquisadores': pesquisadores,
        'instituicoes': instituicoes
    })

# Editar projeto
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



# Inscrição de aluno em um projeto
@login_required
def inscricao_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        aluno = request.user.perfil  # Assumindo que o aluno é o perfil do usuário logado
        projeto.alunos.add(aluno)
        projeto.save()
        messages.success(request, 'Inscrição realizada com sucesso.')
        return redirect('detalhes_projeto', projeto_id=projeto_id)
    return render(request, 'projetos/inscricao_projeto.html', {'projeto': projeto})



# Listagem de pesquisadores
@login_required
def listar_pesquisadores(request):
    pesquisadores = Pesquisador.objects.all()
    return render(request, 'pesquisadores/lista_pesquisadores.html', {'pesquisadores': pesquisadores})



# Adicionar novo pesquisador
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
    # Supondo que você queira listar os usuários e seus perfis
    usuarios = Perfil.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def detalhes_usuario(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario_id=usuario_id)  # Ou o nome correto do campo que referencia o usuário

    return render(request, 'usuarios/detalhes_usuario.html', {'perfil': perfil})
