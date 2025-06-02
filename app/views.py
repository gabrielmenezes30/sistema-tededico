# app/views.py
from rest_framework import viewsets
from .models import Presente
from .serializers import PresenteSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlencode
import re # Import regex module for email validation

class PresenteViewSet(viewsets.ModelViewSet):
    queryset = Presente.objects.all()
    serializer_class = PresenteSerializer

@login_required
def criar_presente(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        mensagem = request.POST['mensagem']
        imagem = request.FILES.get('imagem')
        video_url = request.POST.get('video_url')
        cor_fundo = request.POST.get('cor_fundo')
        cor_destaque = request.POST.get('cor_destaque')
        musica_url = request.POST.get('musica_url')

        if cor_fundo and not cor_fundo.startswith('#'): cor_fundo = None
        if cor_destaque and not cor_destaque.startswith('#'): cor_destaque = None

        p = Presente(
            autor=request.user,
            titulo=titulo,
            mensagem=mensagem,
            imagem=imagem,
            video_url=video_url,
            cor_fundo=cor_fundo if cor_fundo else None,
            cor_destaque=cor_destaque if cor_destaque else None,
            musica_url=musica_url if musica_url else None,
            status_aprovacao='pendente'
        )
        p.save()

        numero_whatsapp_admin = "5587981493976"
        texto_mensagem = f"Olá! Acabei de criar um presente no Te Dedico (ID: {p.id}) e gostaria de informações para o pagamento de R$ 5,00 para aprovação."
        link_whatsapp = f"https://wa.me/{numero_whatsapp_admin}?{urlencode({'text': texto_mensagem})}"

        return render(request, 'aguardando_aprovaçao.html', {'link_whatsapp': link_whatsapp, 'presente_id': p.id})

    return render(request, 'criar.html')

def ver_presente(request, id):
    presente = get_object_or_404(Presente, pk=id)

    if presente.status_aprovacao != 'aprovado':
        if not (request.user.is_authenticated and (request.user == presente.autor or request.user.is_staff)):
            numero_whatsapp_admin = "87981493976"
            texto_mensagem = f"Olá! Gostaria de informações sobre o pagamento para o presente Te Dedico (ID: {presente.id}). Valor: R$ 5,00."
            link_whatsapp = f"https://wa.me/{numero_whatsapp_admin}?{urlencode({'text': texto_mensagem})}"
            return render(request, 'aguardando_aprovaçao.html', {'link_whatsapp': link_whatsapp, 'presente_id': presente.id})

    return render(request, 'ver.html', {'presente': presente})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'erro': 'Credenciais inválidas'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'] # Get the email
        password = request.POST['password']

        # Basic email format validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render(request, 'register.html', {'erro': 'Por favor, insira um email válido.'}) #

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'erro': 'Usuário já existe'}) #
        
        if User.objects.filter(email=email).exists(): # Check if email already exists
            return render(request, 'register.html', {'erro': 'Este email já está registrado. Por favor, use outro ou faça login.'}) #

        user = User.objects.create_user(username=username, email=email, password=password) # Create user with email
        login(request, user)
        return redirect('/')
    return render(request, 'register.html')

@login_required
def dashboard_view(request):
    presentes_list = Presente.objects.filter(autor=request.user).order_by('-criado_em')
    paginator = Paginator(presentes_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_presentes': presentes_list.count()
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def minha_conta_view(request):
    username = request.user.username
    context = {
        'username': username
    }
    return render(request, 'minhaConta/minha_conta.html', context)