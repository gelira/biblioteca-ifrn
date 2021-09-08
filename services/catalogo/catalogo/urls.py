"""catalogo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from catalogoapp import views

router = SimpleRouter(trailing_slash=False)
router.register('livros', views.LivroViewSet)
router.register('indexadores', views.IndexadorViewSet)
router.register('exemplares', views.ExemplarViewSet)
router.register('localizacoes-fisicas', views.LocalizacaoFisicaViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
