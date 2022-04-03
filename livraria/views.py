from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Livro
from django.core.paginator import Paginator
from random import choice
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    objetos = Livro.objects.order_by('-id')
    destaque_ramdomico = choice(list(objetos))
    page = Paginator(objetos, 12)
    pegapagina = request.GET.get('page')
    paginas = page.get_page(pegapagina)
    return render(request, 'index.html', {
        'livros': paginas,
        'destaque': destaque_ramdomico
    })


def verlivro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    return render(request, 'verlivro.html', {
        'livro': livro
    })


def busca(request):
    termobusca = request.GET.get('termo')
    if termobusca is None or not termobusca:
        messages.add_message(request, messages.ERROR, 'Campo Vazio!')
        return redirect('index')

    camposunidos = Concat('titulo', Value(' '), 'autor')
    objetos = Livro.objects.annotate(
        tituloeautor=camposunidos
    ).filter(
        Q(tituloeautor=termobusca) | Q(titulo__icontains=termobusca) | Q(autor__icontains=termobusca)
        )
        
    try:
        destaque_ramdomico = choice(list(objetos))
        page = Paginator(objetos, 12)
        pegapagina = request.GET.get('page')
        paginas = page.get_page(pegapagina)
        messages.add_message(request, messages.INFO, 'Resultados para {}'.format(termobusca))
        return render(request, 'busca.html', {
            'livros': paginas,
            'destaque': destaque_ramdomico
        })
    except:
        messages.add_message(request, messages.INFO, 'Nada encontrado!')
        return redirect('index')
        
        
