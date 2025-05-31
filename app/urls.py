# app/urls.py
from django.urls import path
from .views import (
    criar_presente,
    ver_presente,
    login_view,
    logout_view,
    register_view,
    dashboard_view  # Importar a nova view
)

urlpatterns = [
    # Mudar a rota principal para o dashboard pode ser uma boa ideia
    path('', dashboard_view, name='dashboard'), 
    path('criar/', criar_presente, name='criar_presente'), # Ajustar a URL de criação
    path('presente/<int:id>/', ver_presente, name='ver_presente'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]