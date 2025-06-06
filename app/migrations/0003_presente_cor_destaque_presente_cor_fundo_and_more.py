# Generated by Django 5.2.1 on 2025-05-31 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_presente_options_presente_autor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='presente',
            name='cor_destaque',
            field=models.CharField(blank=True, help_text='Ex: #FF69B4 para rosa. Deixe em branco para usar o padrão.', max_length=7, null=True, verbose_name='Cor de Destaque'),
        ),
        migrations.AddField(
            model_name='presente',
            name='cor_fundo',
            field=models.CharField(blank=True, help_text='Ex: #FFFFFF para branco. Deixe em branco para usar o padrão.', max_length=7, null=True, verbose_name='Cor de Fundo'),
        ),
        migrations.AddField(
            model_name='presente',
            name='musica_url',
            field=models.URLField(blank=True, help_text='Link direto para um arquivo de áudio (ex: .mp3) ou serviço de streaming compatível.', null=True, verbose_name='URL da Música de Fundo'),
        ),
    ]
