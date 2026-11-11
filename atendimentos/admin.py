from django.contrib import admin

from .models import Atendimento, Cliente, Equipamento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "bairro", "cidade", "tipo")
    list_filter = ("bairro", "cidade", "tipo")
    search_fields = ("nome", "telefone", "endereco", "bairro", "cep")


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = (
        "modelo",
        "capacidade_btu",
        "local_instalado",
        "cliente",
        "data_instalacao",
    )
    list_filter = ("capacidade_btu",)
    search_fields = ("modelo", "local_instalado", "cliente__nome")


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = (
        "data_prevista",
        "cliente",
        "tipo_servico",
        "situacao",
        "valor",
    )
    list_filter = ("situacao", "tipo_servico", "data_prevista")
    search_fields = ("cliente__nome", "cliente__bairro", "observacoes")
    date_hierarchy = "data_prevista"
