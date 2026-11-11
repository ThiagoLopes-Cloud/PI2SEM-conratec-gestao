from django.urls import path

from . import views

urlpatterns = [
    path("", views.painel, name="painel"),
    path("clientes/novo/", views.cadastrar_cliente, name="cadastrar_cliente"),
    path("clientes/<int:cliente_id>/", views.ficha_cliente, name="ficha_cliente"),
    path("atendimentos/novo/", views.lancar_atendimento, name="lancar_atendimento"),
]
