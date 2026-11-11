from datetime import timedelta

from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from .models import Atendimento, Cliente

DIAS_DO_PAINEL = 7


def painel(request):
    hoje = timezone.localdate()
    ultimo_dia = hoje + timedelta(days=DIAS_DO_PAINEL)

    proximos = (
        Atendimento.objects.filter(data_prevista__range=(hoje, ultimo_dia))
        .select_related("cliente", "equipamento")
        .order_by("cliente__bairro", "data_prevista", "cliente__nome")
    )

    grupos = {}
    for atendimento in proximos:
        grupos.setdefault(atendimento.cliente.bairro, []).append(atendimento)

    bairros = [
        {"bairro": bairro, "atendimentos": atendimentos, "total": len(atendimentos)}
        for bairro, atendimentos in grupos.items()
    ]

    clientes_por_bairro = list(
        Cliente.objects.values("bairro")
        .annotate(total=Count("id"))
        .order_by("-total", "bairro")
    )
    # A barra do bairro com mais clientes ocupa a largura toda; as demais
    # ficam proporcionais a ela.
    maior_contagem = max((linha["total"] for linha in clientes_por_bairro), default=0)
    for linha in clientes_por_bairro:
        linha["largura"] = round(linha["total"] * 100 / maior_contagem)

    return render(
        request,
        "atendimentos/painel.html",
        {
            "hoje": hoje,
            "ultimo_dia": ultimo_dia,
            "bairros": bairros,
            "total_proximos": proximos.count(),
            "clientes_por_bairro": clientes_por_bairro,
            "total_clientes": sum(linha["total"] for linha in clientes_por_bairro),
        },
    )
