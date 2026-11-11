from django.urls import path

from . import views

urlpatterns = [
    path("", views.painel, name="painel"),
    path("clientes/<int:cliente_id>/", views.ficha_cliente, name="ficha_cliente"),
]
