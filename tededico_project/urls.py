# tededico_project/urls.py

from django.contrib import admin
from django.urls import path, include # Certifique-se de que 'include' está importado
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns # Importe i18n_patterns se for usar tradução de URLs
                                                # ou apenas inclua 'django.conf.urls.i18n'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.api_urls')), #
    path('', include('app.urls')), #
    path('i18n/', include('django.conf.urls.i18n')), # <--- Adicione esta linha

    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #

# Se você planeja ter URLs traduzidas para o restante do site (não apenas o admin),
# você pode configurar i18n_patterns assim:
# urlpatterns += i18n_patterns(
# path('seu_app/', include('app.urls')),
# Adicione outras URLs que você quer que sejam traduzidas aqui
# )