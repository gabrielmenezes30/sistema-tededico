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
from django.utils.http import urlencode # Para formatar a mensagem do WhatsApp

class PresenteViewSet(viewsets.ModelViewSet):
    queryset = Presente.objects.all()
    serializer_class = PresenteSerializer

@login_required #
def criar_presente(request):
    if request.method == 'POST':
        titulo = request.POST['titulo'] #
        mensagem = request.POST['mensagem'] #
        imagem = request.FILES.get('imagem') #
        video_url = request.POST.get('video_url') #
        cor_fundo = request.POST.get('cor_fundo') #
        cor_destaque = request.POST.get('cor_destaque') #
        musica_url = request.POST.get('musica_url') #

        if cor_fundo and not cor_fundo.startswith('#'): cor_fundo = None #
        if cor_destaque and not cor_destaque.startswith('#'): cor_destaque = None #

        p = Presente(
            autor=request.user, #
            titulo=titulo,
            mensagem=mensagem,
            imagem=imagem,
            video_url=video_url,
            cor_fundo=cor_fundo if cor_fundo else None,
            cor_destaque=cor_destaque if cor_destaque else None,
            musica_url=musica_url if musica_url else None,
            status_aprovacao='pendente' # Define o status inicial
        )
        p.save() # Salva o presente no banco

        # ---- Redirecionamento para WhatsApp ----
        numero_whatsapp_admin = "5587981493976"  # Substitua pelo seu número com código do país, ex: 558799999999
        texto_mensagem = f"Olá! Acabei de criar um presente no Te Dedico (ID: {p.id}) e gostaria de informações para o pagamento de R$ 5,00 para aprovação."
        link_whatsapp = f"https://wa.me/{numero_whatsapp_admin}?{urlencode({'text': texto_mensagem})}"

        # Você pode redirecionar diretamente ou para uma página intermediária
        # return redirect(link_whatsapp)
        return render(request, 'aguardando_aprovaçao.html', {'link_whatsapp': link_whatsapp, 'presente_id': p.id})


    return render(request, 'criar.html')

def ver_presente(request, id):
    presente = get_object_or_404(Presente, pk=id) #

    # Se o presente não está aprovado
    if presente.status_aprovacao != 'aprovado':
        # Permitir que o autor ou admin vejam a página de "pendente" ou até o presente em si (para revisão)
        # Se o usuário logado NÃO é o autor E NÃO é staff, mostre a página de "aguardando_aprovacao"
        if not (request.user.is_authenticated and (request.user == presente.autor or request.user.is_staff)):
            # Montar link do WhatsApp novamente para a página de aguardando aprovação
            numero_whatsapp_admin = "87981493976"  # Mantenha este valor consistente ou pegue de settings.py
            texto_mensagem = f"Olá! Gostaria de informações sobre o pagamento para o presente Te Dedico (ID: {presente.id}). Valor: R$ 5,00."
            link_whatsapp = f"https://wa.me/{numero_whatsapp_admin}?{urlencode({'text': texto_mensagem})}"
            return render(request, 'aguardando_aprovacao.html', {'link_whatsapp': link_whatsapp, 'presente_id': presente.id})
        # Se for o autor ou staff, pode continuar para ver o presente, mas o template precisa lidar com o QR code
        # ou você pode ter um template diferente para "pré-visualização de pendente pelo autor/admin".
        # Por simplicidade, vamos deixar o template 'ver.html' lidar com o QR code condicionalmente.

    # Se chegou aqui, o presente está aprovado OU é o autor/staff vendo um presente pendente.
    # O template 'ver.html' precisará de uma condicional para o QR code.
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
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'erro': 'Usuário já existe'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'register.html')

@login_required
def dashboard_view(request):
    # Buscar apenas os presentes criados pelo usuário logado, ordenados pelos mais recentes
    presentes_list = Presente.objects.filter(autor=request.user).order_by('-criado_em')

    # Paginação: mostrar 5 presentes por página (ajuste conforme necessário)
    paginator = Paginator(presentes_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_presentes': presentes_list.count()
    }
    return render(request, 'dashboard/dashboard.html', context) # Novo template