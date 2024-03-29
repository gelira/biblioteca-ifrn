"""gateway URL Configuration

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

from gatewayapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacao/<path:path>', views.AutenticacaoProxyView.as_view()),
    path('catalogo/<path:path>', views.CatalogoProxyView.as_view()),
    path('circulacao/<path:path>', views.CirculacaoProxyView.as_view()),
    path('avaliacao/<path:path>', views.AvaliacaoProxyView.as_view()),
    path('aquisicao/<path:path>', views.AquisicaoProxyView.as_view()),
]
