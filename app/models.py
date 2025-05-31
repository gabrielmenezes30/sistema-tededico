# app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File

class Presente(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presentes", verbose_name="Autor")
    titulo = models.CharField(max_length=255, verbose_name="Título")
    mensagem = models.TextField(verbose_name="Mensagem")
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True, verbose_name="Imagem")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL do Vídeo")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True, verbose_name="QR Code")

    # Novos campos para personalização da aparência
    cor_fundo = models.CharField(
        max_length=7,  # Para código hexadecimal ex: #RRGGBB
        blank=True,
        null=True,
        verbose_name="Cor de Fundo",
        help_text="Ex: #FFFFFF para branco. Deixe em branco para usar o padrão."
    )
    cor_destaque = models.CharField(
        max_length=7,  # Para código hexadecimal ex: #RRGGBB
        blank=True,
        null=True,
        verbose_name="Cor de Destaque",
        help_text="Ex: #FF69B4 para rosa. Deixe em branco para usar o padrão."
    )
    musica_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL da Música de Fundo",
        help_text="Link direto para um arquivo de áudio (ex: .mp3) ou serviço de streaming compatível."
    )

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('ver_presente', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        # Limpar valores de cor se não forem hex válidos (simplificado, pode precisar de validação mais robusta)
        if self.cor_fundo and not self.cor_fundo.startswith('#'):
            self.cor_fundo = None
        if self.cor_destaque and not self.cor_destaque.startswith('#'):
            self.cor_destaque = None

        super().save(*args, **kwargs)

        if is_new or not self.qr_code:
            base_url = getattr(settings, 'SITE_URL_BASE', f"http://127.0.0.1:{getattr(settings, 'DEV_SERVER_PORT', '8000')}")
            presente_url_path = self.get_absolute_url()
            full_url = f"{base_url}{presente_url_path}"

            qr_img = qrcode.make(full_url)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            file_name = f'qrcode_{self.id}.png'
            
            self.qr_code.save(file_name, File(buffer), save=False)
            
            # Coleta os campos que foram originalmente passados para update_fields
            update_fields_param = kwargs.get('update_fields')
            final_update_fields = None

            if not is_new: # Se não for novo, só atualizamos o qr_code e os campos de personalização se necessário
                final_update_fields = ['qr_code']
                # Se update_fields foi especificado, preservamos e adicionamos qr_code
                if update_fields_param is not None:
                    final_update_fields = list(set(list(update_fields_param) + ['qr_code']))
            
            # Chamada de save para o qr_code (e outros campos se for um objeto novo)
            if final_update_fields:
                 super().save(update_fields=final_update_fields)
            else: # Se for novo, salva tudo
                 super().save()


    class Meta:
        verbose_name = "Presente"
        verbose_name_plural = "Presentes"
        ordering = ['-criado_em']