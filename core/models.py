from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)
    instituto = models.CharField(max_length=100)
    foto_perfil = models.ImageField(upload_to='user/fotos_perfil/', blank=True, null=True)

    TIPO_USUARIO_CHOICES = [
        ('Aluno', 'Aluno'),
        ('Professor', 'Professor'),
        ('Pesquisador', 'Pesquisador'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, blank=True, null=True) # o tipo de usuario é opcional, para evitar conflito

    def __str__(self):
        return self.usuario.username


#models para informações das instituições
class Instituicao(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class DuvidaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Dúvida de {self.usuario.username} - {self.data_envio.strftime("%d/%m/%Y")}'


class PesquisaOpiniao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Nota {self.nota} de {self.usuario.username}'

#models para pesquisador e se
class Pesquisador(models.Model):
    nome = models.CharField(max_length=255)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.SET_NULL, null=True)
    contato = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nome



#Models para status do projeto e suas informações

class Projeto(models.Model):
    SITUACAO_CHOICES = [
        ('concluido', 'Concluído'),
        ('andamento', 'Em Andamento'),
        ('planejamento', 'Em Planejamento')
    ]

    titulo = models.CharField(max_length=255)
    resumo = models.TextField()
    resultados = models.TextField(blank=True)
    fotos = models.ImageField(upload_to='projetos/fotos/', blank=True, null=True)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='planejamento')
    descricao = models.TextField(blank=True)
    artigos = models.FileField(upload_to='projetos/artigos/', blank=True, null=True)


    pesquisadores = models.ManyToManyField('Pesquisador')
    instituicoes = models.ManyToManyField('Instituicao')

    alunos = models.ManyToManyField('Perfil', related_name='projetos', blank=True)

    def __str__(self):
        return self.titulo



#models parceiros
class Parceiro(models.Model):
    nome = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='parceiros/logos/', blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.nome

#models de imagens
class ImagemSite(models.Model):
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='site_images/')
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.titulo
