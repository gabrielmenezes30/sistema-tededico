from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class Presente(models.Model):
    titulo = models.CharField(max_length=255)
    mensagem = models.TextField()
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        url = f"https://127.0.0.1:8000/presente/{self.id}/"
        qr = qrcode.make(url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        self.qr_code.save(f'qrcode_{self.id}.png', File(buffer), save=False)
        super().save(*args, **kwargs)