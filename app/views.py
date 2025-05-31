from rest_framework import viewsets
from .models import Presente
from .serializers import PresenteSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
        p = Presente(titulo=titulo, mensagem=mensagem, imagem=imagem, video_url=video_url)
        p.save()
        return HttpResponseRedirect(f'/presente/{p.id}/')
    return render(request, 'criar.html')

def ver_presente(request, id):
    presente = get_object_or_404(Presente, pk=id)
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