# app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
import uuid # For generating unique tokens
from django.utils import timezone # For managing expiry


class Presente(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presentes", verbose_name="Autor") #
    titulo = models.CharField(max_length=255, verbose_name="Título") #
    mensagem = models.TextField(verbose_name="Mensagem") #
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True, verbose_name="Imagem") #
    video_url = models.URLField(blank=True, null=True, verbose_name="URL do Vídeo") #
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em") #
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True, verbose_name="QR Code") #
    cor_fundo = models.CharField(max_length=7, blank=True, null=True, verbose_name="Cor de Fundo", help_text="Ex: #FFFFFF para branco. Deixe em branco para usar o padrão.") #
    cor_destaque = models.CharField(max_length=7, blank=True, null=True, verbose_name="Cor de Destaque", help_text="Ex: #FF69B4 para rosa. Deixe em branco para usar o padrão.") #
    musica_url = models.URLField(blank=True, null=True, verbose_name="URL da Música de Fundo", help_text="Link direto para um arquivo de áudio (ex: .mp3) ou serviço de streaming compatível.") #

    STATUS_CHOICES = [
        ('pendente', 'Pendente de Aprovação'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    status_aprovacao = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status da Aprovação"
    )

    def __str__(self):
        return self.titulo #

    def get_absolute_url(self):
        return reverse('ver_presente', kwargs={'id': self.id}) #

    def save(self, *args, **kwargs):
        # Limpar cores se inválidas
        if self.cor_fundo and not self.cor_fundo.startswith('#'): self.cor_fundo = None #
        if self.cor_destaque and not self.cor_destaque.startswith('#'): self.cor_destaque = None #

        # Salva o objeto (necessário para ter um ID se for novo)
        # e para registrar a mudança de status antes de gerar o QR code.
        super().save(*args, **kwargs)

        # Gerar QR Code APENAS se o status for 'aprovado' e (não houver QR code OU se o QR code precisa ser recriado por alguma razão)
        # A lógica mais simples é gerar se 'aprovado' e não existe.
        # Se você precisar que o QR code seja regerado se a URL do presente mudar por algum motivo (improvável aqui),
        # a lógica seria mais complexa.
        if self.status_aprovacao == 'aprovado' and not self.qr_code:
            base_url = getattr(settings, 'SITE_URL_BASE', f"http://127.0.0.1:{getattr(settings, 'DEV_SERVER_PORT', '8000')}") #
            presente_url_path = self.get_absolute_url()
            full_url = f"{base_url}{presente_url_path}"

            qr_img = qrcode.make(full_url)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            file_name = f'qrcode_{self.id}.png'

            self.qr_code.save(file_name, File(buffer), save=False) # Atribui ao campo
            # Chama super().save() novamente APENAS para salvar o campo qr_code
            # É crucial usar update_fields para evitar chamadas recursivas infinitas se outras lógicas no save()
            # pudessem ser acionadas novamente.
            super().save(update_fields=['qr_code'])

    class Meta:
        verbose_name = "Presente" #
        verbose_name_plural = "Presentes" #
        ordering = ['-criado_em'] #