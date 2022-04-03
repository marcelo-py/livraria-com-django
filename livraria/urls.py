from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('busca/', views.busca, name='busca'),
    path('<int:livro_id>', views.verlivro, name='verlivro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
