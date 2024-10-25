from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import PesquisaOpiniao, Projeto, Pesquisador, Instituicao
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone

from . import models
from .forms import RegistroUsuarioForm, PerfilForm, TipoUsuarioForm, PerfilAdminForm, DuvidaForm, \
    PesquisaOpiniaoForm, ProjetoForm
from .models import Perfil, Parceiro, DuvidaUsuario
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

def editar_perfil(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario__id=usuario_id)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        tipo_usuario_form = TipoUsuarioForm(request.POST, instance=perfil) if request.user.is_staff else None

        if request.user.is_staff:
            if form.is_valid() and tipo_usuario_form.is_valid():
                form.save()
                tipo_usuario_form.save()  # Salva o tipo de usuário se for admin
                messages.success(request, 'Perfil e tipo de usuário atualizados com sucesso!')
                return redirect('detalhes_usuario', usuario_id=usuario_id)
            else:
                messages.error(request, 'Erro ao atualizar o perfil ou tipo de usuário.')
        else:
            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('detalhes_usuario', usuario_id=usuario_id)
            else:
                messages.error(request, 'Erro ao atualizar o perfil.')

    else:
        form = PerfilForm(instance=perfil)
        tipo_usuario_form = TipoUsuarioForm(instance=perfil) if request.user.is_staff else None

    # Redireciona para o template correto
    if request.user.is_staff:
        return render(request, 'admin-editUser.html', {'form': form, 'tipo_usuario_form': tipo_usuario_form, 'perfil': perfil})
    else:
        return render(request, 'usuarios/editar_perfil.html', {'form': form, 'perfil': perfil})

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


# Projetos marcados pelo admin como "Em Andamento"
def projetos_andamento(request):
    pesquisa= request.GET.get('pesquisa')
    print(pesquisa)
    if pesquisa:
        projetos_andamento = Projeto.objects.filter(situacao='andamento', titulo__icontains=pesquisa)
    else:
        projetos_andamento = Projeto.objects.filter(situacao='andamento')
    return render(request, 'projetos/projetos_andamento.html', {'projetos_andamento': projetos_andamento})

# Projetos marcados pelo admin como "Concluídos"
def projetos_concluidos(request):
    pesquisa=request.GET.get('pesquisa')
    print(pesquisa)
    if pesquisa:
        projetos_concluidos = Projeto.objects.filter(situacao='concluidos', titulo__icontains=pesquisa)
    else:
        projetos_concluidos = Projeto.objects.filter(situacao='concluidos')
    return render(request, 'projetos/projetos_concluido.html', {'projetos_concluidos': projetos_concluidos})

# Projetos marcados pelo admin como "Em Planejamento"
def projetos_iniciados(request):
    pesquisa=request.GET.get('pesquisa')
    print(pesquisa)
    if pesquisa:
        projetos_iniciados = Projeto.objects.filter(situacao='planejamento', titulo__icontains=pesquisa)
    else:
        projetos_iniciados = Projeto.objects.filter(situacao='planejamento')
    return render(request, 'projetos/projetos_iniciados.html', {'projetos_iniciados': projetos_iniciados})

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
        if request.user.id == perfil.usuario.id:

            form = PerfilForm(request.POST, request.FILES, instance=perfil)
        else:

            form = PerfilAdminForm(request.POST, request.FILES, instance=perfil)

        if 'foto_perfil' in request.FILES:
            print("Arquivo de imagem enviado:", request.FILES['foto_perfil'])
        else:
            print("Nenhuma imagem enviada")

        if form.is_valid():
            form.save()
            if perfil.foto_perfil:
                print(f"Imagem salva com sucesso: {perfil.foto_perfil.url}")
            else:
                print("Erro ao salvar a imagem")

            return redirect('detalhes_usuario', usuario_id=usuario_id)
        else:
            print("Formulário inválido. Erros:", form.errors)
    else:
        if request.user.id == perfil.usuario.id:
            form = PerfilForm(instance=perfil)
        else:
            form = PerfilAdminForm(instance=perfil)

    return render(request, 'usuarios/editardetalhes.html', {'form': form, 'perfil': perfil})

def editar_detalhes(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario__id=usuario_id)

    # Verifique se o usuário atual está editando seu próprio perfil
    if request.user.id == perfil.usuario.id:
        # Formulário normal para usuários comuns
        form = PerfilForm(instance=perfil)
    else:
        # Formulário para administradores
        form = PerfilAdminForm(instance=perfil)

    if request.method == 'POST':
        if request.user.id == perfil.usuario.id:
            form = PerfilForm(request.POST, request.FILES, instance=perfil)
        else:
            form = PerfilAdminForm(request.POST, request.FILES, instance=perfil)

        if form.is_valid():
            form.save()
            messages.success(request, 'As informações foram atualizadas com sucesso!')
            return redirect('detalhes_usuario', usuario_id=usuario_id)
        else:
            print(form.errors)

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


            if user.is_superuser or user.is_staff:

                return redirect('admin_dashboard')
            else:

                return redirect('index')
        else:

            messages.error(request, 'Credenciais inválidas.')
            return render(request, 'login.html')

    return render(request, 'login.html')


# verificando se é administrador
def admin_check(user):
    return user.is_staff or user.is_superuser


class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('admin_dashboard')
        return reverse('inicio')


# função para verificar se o usuário é admin (is_staff)
def is_admin(user):
    return user.is_staff

# view que controla a rota apenas admins (é o que é mostrado se entrar como admin do terminal)
@user_passes_test(is_admin)
@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin/dashboardAdmin.html')



# Listar Projetos  PARA O ADMIN, SOMENTE.
def listar_projetos(request):
    projetos = Projeto.objects.all()
    return render(request, 'admin/lista_projetos.html', {'projetos': projetos})
#


# Editar Projeto
@staff_member_required
def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if request.method == 'POST':
        projeto.titulo = request.POST.get('titulo')
        projeto.resumo = request.POST.get('resumo')
        projeto.resultados = request.POST.get('resultados')
        projeto.situacao = request.POST.get('situacao')
        projeto.descricao = request.POST.get('descricao')
        projeto.fotos = request.FILES.get('fotos', projeto.fotos)  # vai manter a foto padrão se não nova não for enviada
        projeto.save()
        messages.success(request, 'Projeto atualizado com sucesso.')
        return redirect('listar_projetos')

    return render(request, 'admin/editar_projeto.html', {'projeto': projeto})

# Deletar Projeto
@staff_member_required
def deletar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    projeto.delete()
    messages.success(request, 'Projeto deletado com sucesso.')
    return redirect('listar_projetos')


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
        # Coletando os dados do formulário
        titulo = request.POST.get('titulo')
        resumo = request.POST.get('resumo')
        resultados = request.POST.get('resultados')
        situacao = request.POST.get('situacao')
        descricao = request.POST.get('descricao')

        # Obtendo arquivos de fotos e artigos, se houver
        fotos = request.FILES.getlist('fotos')  # Mudança para lidar com múltiplos arquivos
        artigos = request.FILES.getlist('artigos')  # Mudança para lidar com múltiplos arquivos

        # Criando o objeto Projeto
        projeto = Projeto.objects.create(
            titulo=titulo,
            resumo=resumo,
            resultados=resultados,
            situacao=situacao,
            descricao=descricao,
        )

        # Adicionando múltiplas fotos e artigos ao projeto
        for foto in fotos:
            projeto.fotos = foto  # Ajustar se necessário para salvar múltiplas imagens de maneira personalizada
            projeto.save()

        for artigo in artigos:
            projeto.artigos = artigo  # Ajustar se necessário para salvar múltiplos artigos de maneira personalizada
            projeto.save()

        # Adicionando Pesquisadores
        pesquisadores = request.POST.getlist('pesquisadores')
        for pesquisador_id in pesquisadores:
            pesquisador = Pesquisador.objects.get(id=pesquisador_id)
            projeto.pesquisadores.add(pesquisador)

        # Adicionando Instituições
        instituicoes = request.POST.getlist('instituicoes')
        for instituicao_id in instituicoes:
            instituicao = Instituicao.objects.get(id=instituicao_id)
            projeto.instituicoes.add(instituicao)

        # Adicionando Alunos
        alunos = request.POST.getlist('alunos')
        for aluno_id in alunos:
            aluno = Perfil.objects.get(id=aluno_id)
            projeto.alunos.add(aluno)

        # Salvando o projeto com todas as associações
        projeto.save()

        # Mensagem de sucesso e redirecionamento
        messages.success(request, 'Projeto cadastrado com sucesso.')
        return redirect('listar_projetos')

    # Carregando os dados para o formulário
    pesquisadores = Pesquisador.objects.all()
    instituicoes = Instituicao.objects.all()
    alunos = Perfil.objects.filter(tipo_usuario='aluno')  # Filtrando perfis de alunos

    # Renderizando o template de adicionar projeto
    return render(request, 'projetos/adicionar_projeto.html', {
        'pesquisadores': pesquisadores,
        'instituicoes': instituicoes,
        'alunos': alunos
    })
#  admin  editar um projeto


@staff_member_required
@login_required
def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            projeto = form.save(commit=False)  # Salva sem persistir ainda

            # Limpa as relações existentes
            projeto.pesquisadores.clear()
            projeto.instituicoes.clear()

            # Atualiza os pesquisadores
            pesquisadores = request.POST.getlist('pesquisadores')
            for pesquisador_id in pesquisadores:
                projeto.pesquisadores.add(Pesquisador.objects.get(id=pesquisador_id))

            # Atualiza os professores (corrigindo a variável)
            professores = request.POST.getlist('professores')
            for professor_id in professores:
                projeto.pesquisadores.add(Pesquisador.objects.get(id=professor_id))

            # Atualiza as instituições
            instituicoes = request.POST.getlist('instituicoes')
            for instituicao_id in instituicoes:
                projeto.instituicoes.add(Instituicao.objects.get(id=instituicao_id))

            # Salva as mudanças no banco de dados
            projeto.save()
            messages.success(request, 'Projeto atualizado com sucesso.')
            return redirect('listar_projetos')
    else:
        form = ProjetoForm(instance=projeto)

    # Carrega os dados necessários para o template
    pesquisadores = Pesquisador.objects.all()
    instituicoes = Instituicao.objects.all()

    return render(request, 'admin/editar_projeto.html', {
        'form': form,
        'projeto': projeto,
        'pesquisadores': pesquisadores,
        'instituicoes': instituicoes,
    })


# view para deletar o projeto
@login_required
def deletar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == 'POST':
        projeto.delete()
        messages.success(request, 'Projeto deletado com sucesso.')
        return redirect('listar_projetos')
    return render(request, 'admin/deletar_projeto.html', {'projeto': projeto})




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



@staff_member_required
def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(Perfil, user_id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário deletado com sucesso.')
        return redirect('lista_usuarios')

    return render(request, 'usuarios/deletar_usuario.html', {'usuario': usuario})


@staff_member_required
def editar_usuario(request, usuario_id):
    perfil = get_object_or_404(Perfil, user_id=usuario_id)

    if request.method == 'POST':
        novo_tipo = request.POST.get('tipo_usuario')
        if novo_tipo in ['comum', 'pesquisador', 'parceiro']:
            perfil.tipo_usuario = novo_tipo
            perfil.save()
            messages.success(request, 'Tipo de usuário atualizado com sucesso.')
            return redirect('detalhes_usuario', usuario_id=usuario_id)  #salva

    return render(request, 'editar_detalhes_usuario.html', {'perfil': perfil})



@login_required
def enviar_duvida(request):
    mensagem = ""
    if request.method == 'POST':

        usuario = request.user
        mensagem_duvida = request.POST.get('mensagem')

        DuvidaUsuario.objects.create(usuario=usuario, mensagem=mensagem_duvida)

        mensagem = "Enviado. Agradecemos por enviar sua dúvida!"

    return render(request, 'usuarios/enviar_duvida.html', {'mensagem': mensagem})


@login_required
def listar_duvidas(request):
    duvidas = DuvidaUsuario.objects.all().order_by('-data_envio')
    return render(request, 'admin/duvidas_usuarios.html', {'duvidas': duvidas})


@login_required
def pesquisa_opiniao(request):
    if request.method == 'POST':
        form = PesquisaOpiniaoForm(request.POST)
        if form.is_valid():
            pesquisa = form.save(commit=False)
            pesquisa.usuario = request.user
            pesquisa.data_envio = timezone.now()
            pesquisa.save()

            mensagem = "Obrigado pela sua opinião! Agradecemos pelo feedback."
            return render(request, 'usuarios/pesquisa_opiniao.html', {'form': form, 'mensagem': mensagem})
    else:
        if PesquisaOpiniao.objects.filter(usuario=request.user).exists():

            return redirect('pesquisa_opiniao')
        form = PesquisaOpiniaoForm()

    return render(request, 'usuarios/pesquisa_opiniao.html', {'form': form})


def resultados_pesquisa(request):
    todas_notas = PesquisaOpiniao.objects.values('nota').annotate(total=Count('nota')).order_by('nota')
    media_notas = PesquisaOpiniao.objects.all().aggregate(media=Avg('nota'))['media']

    contexto = {
        'todas_notas': todas_notas,
        'media_notas': media_notas,
    }

    return render(request, 'admin/pesquisa_opiniao_usuario.html', contexto)
