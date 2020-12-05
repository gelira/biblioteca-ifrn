"""autenticacao URL Configuration

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
from rest_framework.routers import SimpleRouter

from autenticacaoapp import views

router = SimpleRouter(trailing_slash=False)
router.register('perfis', views.PerfilViewSet)
router.register('promocao', views.PromocaoViewSet)

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('token', views.ObterTokenView.as_view()),
    path('token-local', views.ObterTokenLocalView.as_view()),
    path('verificar', views.VerificarTokenView.as_view()),
    path('informacoes', views.InformacoesUsuarioView.as_view()),
    path('consulta', views.ConsultaUsuarioView.as_view()),
    path('suspensoes', views.UsuariosSuspensosView.as_view()),
    path('abonos', views.UsuariosAbonoView.as_view()),
] + router.urls
