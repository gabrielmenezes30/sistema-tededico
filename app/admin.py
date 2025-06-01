# app/admin.py
from django.contrib import admin #
from .models import Presente #

@admin.register(Presente) #
class PresenteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'criado_em', 'status_aprovacao', 'imagem_preview', 'video_url') #
    list_filter = ('autor', 'criado_em', 'status_aprovacao') #
    search_fields = ('titulo', 'mensagem', 'autor__username') #
    readonly_fields = ('qr_code_preview', 'criado_em') #
    fieldsets = (
        (None, {
            'fields': ('autor', 'titulo', 'mensagem', 'status_aprovacao') # Adicionado status_aprovacao
        }),
        ('Mídia', {
            'fields': ('imagem', 'video_url', 'musica_url') # Adicionado musica_url
        }),
         ('Personalização Visual', { # Nova seção para cores
            'fields': ('cor_fundo', 'cor_destaque'),
            'classes': ('collapse',), # Opcional: torna a seção recolhível
        }),
        ('QR Code (Gerado Automaticamente Após Aprovação)', { #
            'fields': ('qr_code_preview', 'qr_code'),
        }),
    )
    # ... imagem_preview e qr_code_preview como antes ...
    def imagem_preview(self, obj): #
        from django.utils.html import format_html
        if obj.imagem:
            return format_html('<img src="{}" width="100" height="auto" />', obj.imagem.url)
        return "Sem imagem"
    imagem_preview.short_description = 'Prévia da Imagem' #

    def qr_code_preview(self, obj): #
        from django.utils.html import format_html
        if obj.qr_code:
            return format_html('<img src="{}" width="150" height="150" />', obj.qr_code.url)
        return "QR Code ainda não gerado ou presente pendente" # Mensagem ajustada
    qr_code_preview.short_description = 'Prévia do QR Code' #