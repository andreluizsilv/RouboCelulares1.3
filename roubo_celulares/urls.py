from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página inicial ou mapa de roubos
    path('', views.mapa_roubos, name='mapa_roubos'),

    # Rota para a página de detalhes de uma ocorrência específica
    path('detalhes/<int:id>/', views.detalhes_ocorrencia, name='detalhes_ocorrencia'),

    # Rotas para feedback
    path('feedback/', views.feedback, name='feedback'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),

    # Rota para listar bairros (disponível apenas para usuários autenticados)
    path('bairros/', views.listar_bairros, name='listar_bairros'),

    # Rota para editar bairros (disponível apenas para usuários autenticados)
    path('bairros/editar/<int:bairro_id>/', views.editar_bairro, name='editar_bairro'),

    # Rota para deletar bairro (disponível apenas para usuários autenticados)
    path('bairros/deletar/<int:bairro_id>/', views.deletar_bairro, name='deletar_bairro'),
]
