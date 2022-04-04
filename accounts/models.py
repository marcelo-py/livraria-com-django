from django.db import models
from livraria.models import Livro
from django import forms


class FormLivro(forms.ModelForm):
    class Meta:
        model = Livro
        exclude = ('adcionado',)

