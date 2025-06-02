
from django.urls import path
from .views import (
    criar_presente,
    ver_presente,
    login_view,
    logout_view,
    register_view,
    dashboard_view,
    minha_conta_view,
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('criar/', criar_presente, name='criar_presente'),
    path('presente/<int:id>/', ver_presente, name='ver_presente'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('minha-conta/', minha_conta_view, name='minha_conta'),
]