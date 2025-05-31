# app/models.py
from django.db import models
from django.contrib.auth.models import User # Importar o modelo User
from django.urls import reverse # Para gerar URLs de forma mais dinâmica
from django.conf import settings # Para buscar configurações do projeto
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

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        """Retorna a URL para visualizar este presente."""
        return reverse('ver_presente', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        # Salva o objeto primeiro para garantir que temos um ID, especialmente para novos objetos.
        # Se for uma atualização e o qr_code já existe, não precisamos fazer nada aqui inicialmente.
        is_new = self.pk is None
        super().save(*args, **kwargs) # Primeira chamada para obter o ID se for novo

        # Gerar QR code se for um novo presente ou se o campo qr_code estiver vazio.
        if is_new or not self.qr_code:
            # Construir a URL completa para o QR Code
            # Em produção, configure SITE_URL_BASE no settings.py (ex: 'https://seusite.com')
            # Para desenvolvimento, pode ser 'http://127.0.0.1:8000'
            base_url = getattr(settings, 'SITE_URL_BASE', f"http://127.0.0.1:{getattr(settings, 'DEV_SERVER_PORT', '8000')}")
            presente_url_path = self.get_absolute_url()
            full_url = f"{base_url}{presente_url_path}"

            qr_img = qrcode.make(full_url)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            file_name = f'qrcode_{self.id}.png'
            
            # Usamos save=False na atribuição do campo para evitar loop de save,
            # e então chamamos super().save() novamente apenas para atualizar este campo.
            self.qr_code.save(file_name, File(buffer), save=False)
            
            # Precisamos chamar super().save() novamente para salvar o qr_code.
            # Para evitar recursão e salvar apenas os campos necessários:
            # Coletamos os campos que foram originalmente passados para update_fields
            update_fields = kwargs.get('update_fields')
            if update_fields is not None:
                # Se update_fields foi especificado, adicionamos 'qr_code' a ele
                # Convertendo para lista para poder adicionar, caso seja uma tupla.
                update_fields = list(update_fields) + ['qr_code']
                # Removendo duplicatas caso 'qr_code' já estivesse lá.
                update_fields = list(set(update_fields))
            else:
                # Se update_fields não foi especificado, o Django salvará todos os campos.
                # Nesse caso, como já fizemos um super().save() antes,
                # e estamos apenas atualizando o qr_code, podemos ser explícitos.
                # No entanto, se outros campos foram modificados antes desta lógica de QR Code
                # e não queremos perder essas mudanças, é mais seguro não especificar update_fields
                # ou ter certeza que todos os campos modificados estão incluídos.
                # Por simplicidade aqui, se 'update_fields' não foi usado, deixamos o Django
                # salvar tudo novamente. Ou, para ser mais preciso em uma segunda chamada:
                if not is_new: # Se não for novo, só atualizamos o qr_code.
                     kwargs['update_fields'] = ['qr_code']


            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Presente"
        verbose_name_plural = "Presentes"
        ordering = ['-criado_em']