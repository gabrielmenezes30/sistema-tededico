# app/admin.py
from django.contrib import admin
from .models import Presente

@admin.register(Presente)
class PresenteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'criado_em', 'imagem_preview', 'video_url')
    list_filter = ('autor', 'criado_em')
    search_fields = ('titulo', 'mensagem', 'autor__username')
    readonly_fields = ('qr_code_preview', 'criado_em') # Adicionado criado_em aqui também
    fieldsets = (
        (None, {
            'fields': ('autor', 'titulo', 'mensagem')
        }),
        ('Mídia', {
            'fields': ('imagem', 'video_url')
        }),
        ('QR Code (Gerado Automaticamente)', {
            'fields': ('qr_code_preview', 'qr_code'), # Mostrar o QR Code e o campo
        }),
    )

    def imagem_preview(self, obj):
        from django.utils.html import format_html
        if obj.imagem:
            return format_html('<img src="{}" width="100" height="auto" />', obj.imagem.url)
        return "Sem imagem"
    imagem_preview.short_description = 'Prévia da Imagem'

    def qr_code_preview(self, obj):
        from django.utils.html import format_html
        if obj.qr_code:
            return format_html('<img src="{}" width="150" height="150" />', obj.qr_code.url)
        return "QR Code ainda não gerado"
    qr_code_preview.short_description = 'Prévia do QR Code'