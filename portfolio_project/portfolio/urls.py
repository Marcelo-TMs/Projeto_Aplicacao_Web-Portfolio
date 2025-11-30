from django.urls import path
from . import views
from .views import signup

urlpatterns = [
    path('', views.listar_projetos, name='listar_projetos'),
    path('projeto/novo/', views.criar_projeto, name='criar_projeto'),
    path('projeto/<int:id>/editar/', views.editar_projeto, name='editar_projeto'),
    path('projeto/<int:id>/excluir/', views.excluir_projeto, name='excluir_projeto'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<str:username>/', views.perfil_publico, name='perfil_publico'),
    path('signup/', signup, name='signup'),
    path('projeto/<int:id>/', views.detalhe_projeto, name='detalhe_projeto'),
    path('sobre/', views.sobre, name='sobre'),
]
