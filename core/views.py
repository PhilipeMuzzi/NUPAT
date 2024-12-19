import logging

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import PesquisaOpiniao, Projeto, Pesquisador, Instituicao
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from .forms import RegistroUsuarioForm, PerfilForm, TipoUsuarioForm, PerfilAdminForm, \
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

def \
        editar_perfil(request, usuario_id):
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

    if request.user.is_staff:
        return render(request, 'admin-editUser.html', {'form': form, 'tipo_usuario_form': tipo_usuario_form, 'perfil': perfil})
    else:
        return render(request, 'usuarios/editar_perfil.html', {'form': form, 'perfil': perfil})

def inicio(request):
    # traz os 6 últimos projetos mais recentes para a primeira seção
    ultimos_projetos = Projeto.objects.order_by('-id')[:6]

    return render(request,'index.html', {
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
    return render(request, 'projetos/todos_projetos.html', {'projetos_andamento': projetos_andamento})

# Projetos marcados pelo admin como "Concluídos"
def projetos_concluidos(request):
    pesquisa=request.GET.get('pesquisa')
    print(pesquisa)
    if pesquisa:
        projetos_concluidos = Projeto.objects.filter(situacao='concluido', titulo__icontains=pesquisa)
    else:
        projetos_concluidos = Projeto.objects.filter(situacao='concluido')
    return render(request, 'projetos/projetos_concluidos.html', {'projetos_concluidos': projetos_concluidos})

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
            return redirect('login')
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

    if request.user.id == perfil.usuario.id:

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
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Autentica com o email

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

    total_usuarios = User.objects.filter(is_active=True).count()
    total_projetos = Projeto.objects.count()
    context = {
        'total_usuarios': total_usuarios,
        'total_projetos': total_projetos,
    }
    return render(request, 'admin/dashboardAdmin.html', context)


# Listar Projetos  PARA O ADMIN, SOMENTE.
def listar_projetos(request):
    projetos = Projeto.objects.all()
    return render(request, 'admin/lista_projetos.html', {'projetos': projetos})


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
    pesquisadores = projeto.pesquisadores.all()
    return render(request, 'projetos/detalhes_projeto.html', {
        'projeto': projeto,
        'alunos': alunos,
        'parceiros': pesquisadores,

    })

@login_required
def criar_instituicao(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        departamento = request.POST.get('departamento')

        if nome and endereco and departamento:
            instituicao = Instituicao(
                nome=nome,
                endereco=endereco,
                departamento=departamento
            )
            instituicao.save()
            messages.success(request, "Instituição criada com sucesso!")
            return redirect('projetos/adicionar_projeto')
        else:
            messages.error(request, "Todos os campos são obrigatórios.")

    return render(request, 'instituicoes/criar_instituicao.html')

@staff_member_required
def adicionar_projeto(request):
    if request.method == "POST":
        form = ProjetoForm(request.POST, request.FILES)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.save()
            form.save_m2m()
            messages.success(request, "Projeto criado com sucesso!")
            return redirect('/')
        else:
            messages.error(request, "Erro ao salvar o projeto. Verifique os campos.")
    else:
        form = ProjetoForm()


    pesquisadores = Perfil.objects.filter(tipo_usuario='Pesquisador')
    professores = Perfil.objects.filter(tipo_usuario='Professor')
    alunos = Perfil.objects.filter(tipo_usuario='Aluno')
    instituicoes = Instituicao.objects.all()


    return render(request, 'projetos/adicionar_projeto.html', {
        'form': form,
        'pesquisadores': pesquisadores,
        'professores': professores,
        'alunos': alunos,
        'instituicoes': instituicoes,
    })

def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            projeto = form.save()
            messages.success(request, "Projeto atualizado com sucesso!")
            return redirect('/')
        else:
            messages.error(request, "Erro ao atualizar o projeto.")
    else:
        form = ProjetoForm(instance=projeto)

    return render(request, 'admin/editar_projeto.html', {'form': form, 'projeto': projeto})

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
@staff_member_required()
@login_required
def lista_usuarios(request):

    search_query = request.GET.get('search', '')

    if search_query:
        usuarios = Perfil.objects.filter(
            Q(usuario__username__icontains=search_query) |
            Q(usuario__email__icontains=search_query)
        )
    else:
        usuarios = Perfil.objects.all()

    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios, 'search_query': search_query})

@login_required
def detalhes_usuario(request, usuario_id):
    perfil = get_object_or_404(Perfil, usuario__id=usuario_id)
    print(perfil.telefone, perfil.endereco, perfil.instituto)

    return render(request, 'usuarios/detalhes_usuario.html', {'perfil': perfil})

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)


@staff_member_required
def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(Perfil, id=usuario_id)

    if request.method == 'POST':

        usuario.usuario.delete()
        messages.success(request, 'Usuário deletado com sucesso.')

    usuarios = Perfil.objects.all()

    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


@staff_member_required
def editar_usuario(request, usuario_id):
    perfil = get_object_or_404(Perfil, user_id=usuario_id)

    if request.method == 'POST':
        novo_tipo = request.POST.get('tipo_usuario')
        if novo_tipo in ['comum', 'pesquisador', 'parceiro']:
            perfil.tipo_usuario = novo_tipo
            perfil.save()
            messages.success(request, 'Tipo de usuário atualizado com sucesso.')
            return redirect('detalhes_usuario', usuario_id=usuario_id)

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

# View para apagar uma dúvida

def apagar_duvida(request):
    if request.method == 'POST':
        duvida_id = request.POST.get('duvida_id')
        duvida = get_object_or_404(DuvidaUsuario, id=duvida_id)
        duvida.delete()
        messages.success(request, 'Dúvida excluída com sucesso!')
    return redirect('listar_duvidas')

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

def projetos_por_status(request, status=None):
    if status:
        projetos = Projeto.objects.filter(situacao=status)
    else:
        projetos = Projeto.objects.all()

    instituicoes = Instituicao.objects.all()
    pesquisadores = Pesquisador.objects.all()

    instituicao_selecionada = request.GET.getlist('instituicoes')
    pesquisador_selecionado = request.GET.getlist('pesquisadores')

    if instituicao_selecionada:
        projetos = projetos.filter(instituicao__id__in=instituicao_selecionada)
    if pesquisador_selecionado:
        projetos = projetos.filter(pesquisadores__id__in=pesquisador_selecionado)


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'projetos/partials/projetos_list.html', {'projetos': projetos})


    return render(request, 'projetos/todos_projetos.html', {
        'projetos': projetos,
        'instituicoes': instituicoes,
        'pesquisadores': pesquisadores,
        'status': status,
    })


#logout
@login_required
def logout_view(request):
    logout(request)
    return render(request,'logged_out.html')
