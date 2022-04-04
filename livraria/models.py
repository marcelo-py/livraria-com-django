from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=50, default='desconhecido')
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    adcionado = models.DateTimeField(default=timezone.now)
    imagem = models.ImageField(blank=True, upload_to='imagens/%Y/%m/%d')
    link_para_ler = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.titulo
