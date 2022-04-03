from django.contrib import admin
from . import models


class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'adcionado', 'categoria')
    list_display_links = ('titulo',)


admin.site.register(models.Livro, LivroAdmin)
admin.site.register(models.Categoria)
