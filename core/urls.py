from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import CustomLoginView, detalhes_usuario, quem_somos, area_suporte, atendimento_virtual

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('contas/', include('django.contrib.auth.urls')),
    path('register', views.registro, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('usuarios/<int:usuario_id>/editar/', views.editar_detalhes, name='editar_detalhes'),
    path('usuarios/<int:usuario_id>/', detalhes_usuario, name='detalhes_usuario'),
    path('quem-somos/', quem_somos, name='quem_somos'),
    path('area-suporte/', area_suporte, name='area_suporte'),
    path('atendimento-virtual/', atendimento_virtual, name='atendimento_virtual'),

    # gerenciamento de usuários
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),

    # links para gerenciamento dos projetos
    path('projetos/', views.listar_projetos, name='listar_projetos'),
    path('projetos/adicionar/', views.adicionar_projeto, name='adicionar_projeto'),
    path('projetos/<int:projeto_id>/', views.detalhes_projeto, name='detalhes_projeto'),
    path('projetos/<int:projeto_id>/editar/', views.editar_projeto, name='editar_projeto'),
    path('projetos/<int:projeto_id>/deletar/', views.deletar_projeto, name='deletar_projeto'),





    # links para gerenciamento dos pesquisadores
    path('pesquisadores/', views.listar_pesquisadores, name='listar_pesquisadores'),
    path('pesquisadores/adicionar/', views.adicionar_pesquisador, name='adicionar_pesquisador'),


    path('pesquisadores/adicionar/', views.adicionar_pesquisador, name='adicionar_pesquisador'),
    path('pesquisadores/editar/<int:pesquisador_id>/', views.editar_projeto, name='editar_pesquisador'),
    path('pesquisadores/deletar/<int:pesquisador_id>/', views.deletar_projeto, name='deletar_pesquisador'),


    # URLs para gerenciamento de parceiros
    path('parceiros/', views.listar_parceiros, name='listar_parceiros'),
    path('parceiros/adicionar/', views.adicionar_parceiro, name='adicionar_parceiro'),


    # URLs para gerenciamento de instituições
    path('instituicoes/', views.listar_instituicoes, name='listar_instituicoes'),
    path('instituicoes/adicionar/', views.adicionar_instituicao, name='adicionar_instituicao'),


    # ADMIN
    path('usuarios/editar/<int:usuario_id>/', views.editar_tipo_usuario, name='editar_tipo_usuario'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
