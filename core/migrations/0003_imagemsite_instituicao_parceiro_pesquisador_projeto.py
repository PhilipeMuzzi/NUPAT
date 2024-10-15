# Generated by Django 4.2.13 on 2024-08-17 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_perfil_tipo_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('imagem', models.ImageField(upload_to='site_images/')),
                ('descricao', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instituicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('endereco', models.CharField(max_length=255)),
                ('departamento', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Parceiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='parceiros/logos/')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Pesquisador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('contato', models.CharField(blank=True, max_length=255)),
                ('instituicao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.instituicao')),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('resumo', models.TextField()),
                ('resultados', models.TextField(blank=True)),
                ('fotos', models.ImageField(blank=True, null=True, upload_to='projetos/fotos/')),
                ('situacao', models.CharField(choices=[('concluido', 'Concluído'), ('andamento', 'Em Andamento'), ('planejamento', 'Em Planejamento')], default='planejamento', max_length=20)),
                ('descricao', models.TextField(blank=True)),
                ('artigos', models.FileField(blank=True, null=True, upload_to='projetos/artigos/')),
                ('instituicoes', models.ManyToManyField(to='core.instituicao')),
                ('pesquisadores', models.ManyToManyField(to='core.pesquisador')),
            ],
        ),
    ]
