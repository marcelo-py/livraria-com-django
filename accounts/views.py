from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormLivro
import requests
from json import loads


def login(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')

    if request.method != 'POST':
        if request.GET.get('login'):
            messages.info(request, 'é preciso fazer login para entrar na dashboard!')
        return render(request, 'login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, 'usuario ou Senha inválidos')
        return render(request, 'login.html')

    else:
        auth.login(request, user)
        messages.success(request, 'Logado com sucesso!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index_login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'cadastro.html')

    nome = request.POST.get('nome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode ficar vazio!')
        return render(request, 'cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Opa! email invalido. O campo precisa pelo menos possuir um formato de um.')
        return render(request, 'cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'nome de usuario já existe! tente outro ou faça login')
        return render(request, 'cadastro.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe, use outro ou faça login')
        return render(request, 'cadastro.html')

    #salvando usuario no banco
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome)
    user.save()

    messages.success(request, 'Cadastrado com sucesso! Pronto para logar')
    return redirect('login')


#caso não esteja logado será redirecionado para o template de login para entrar primeiro
@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'dashboard.html')


def addlivro(request):
    if request.method != 'POST':
        form = FormLivro()
        return render(request, 'add_livro.html', {'form': form})

    form = FormLivro(request.POST, request.FILES)

    captcha_token = request.POST.get('g-recaptcha-response')
    cap_url = 'https://www.google.com/recaptcha/api/siteverify'
    cap_secret = '6LddFBcfAAAAAG4tMw8ObV6U_Rw18b4sypadzJe4'
    cap_data = {
        'secret': cap_secret,
        'response': captcha_token}
    cap_server_response = requests.post(url=cap_url, data=cap_data)
    cap_jason = loads(cap_server_response.text)

    if not cap_jason['success']:
        messages.error(request, 'Pergunta de segurança errada!')
        return render(request, 'add_livro.html', {'form': form})

    if not form.is_valid():
        form = FormLivro(request.POST) #vai botar os valores que foram tentados antes
        return render(request, 'add_livro.html', {'form': form})

    descricao = request.POST.get('descricao')
    if len(descricao) < 5:
        messages.error(request, 'A descrição precisa ser maior que 5 caractere')
        return render(request, 'add_livro.html', {'form': form})
    
    messages.success(request, 'Livro {} salvo com sucesso!'.format(request.POST.get('titulo')))
    form.save()
    return redirect('dashboard')

