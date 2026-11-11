from datetime import timedelta

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.formats import date_format

from .forms import AtendimentoForm, ClienteForm, marcar_campos_invalidos
from .models import Atendimento, Cliente

DIAS_DO_PAINEL = 7


def painel(request):
    hoje = timezone.localdate()
    ultimo_dia = hoje + timedelta(days=DIAS_DO_PAINEL)

    agrupar_por_data = request.GET.get("agrupar") == "data"

    if agrupar_por_data:
        ordem = ("data_prevista", "cliente__bairro", "cliente__nome")
    else:
        ordem = ("cliente__bairro", "data_prevista", "cliente__nome")

    proximos = (
        Atendimento.objects.filter(data_prevista__range=(hoje, ultimo_dia))
        .select_related("cliente", "equipamento")
        .order_by(*ordem)
    )

    grupos = {}
    for atendimento in proximos:
        if agrupar_por_data:
            titulo = date_format(atendimento.data_prevista, "l, d/m/Y").capitalize()
        else:
            titulo = atendimento.cliente.bairro
        grupos.setdefault(titulo, []).append(atendimento)

    grupos_do_painel = [
        {"titulo": titulo, "atendimentos": atendimentos, "total": len(atendimentos)}
        for titulo, atendimentos in grupos.items()
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
            "agrupar_por_data": agrupar_por_data,
            "grupos": grupos_do_painel,
            "total_proximos": len(proximos),
            "clientes_por_bairro": clientes_por_bairro,
            "total_clientes": sum(linha["total"] for linha in clientes_por_bairro),
        },
    )


def ficha_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    return render(
        request,
        "atendimentos/ficha_cliente.html",
        {
            "cliente": cliente,
            "equipamentos": cliente.equipamentos.all(),
            "atendimentos": cliente.atendimentos.select_related("equipamento").order_by(
                "-data_prevista"
            ),
        },
    )


def cadastrar_cliente(request):
    if request.method == "POST":
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            cliente = formulario.save()
            return redirect("ficha_cliente", cliente_id=cliente.id)
        marcar_campos_invalidos(formulario)
    else:
        formulario = ClienteForm()

    return render(request, "atendimentos/cliente_form.html", {"formulario": formulario})


def lancar_atendimento(request):
    if request.method == "POST":
        formulario = AtendimentoForm(request.POST)
        if formulario.is_valid():
            atendimento = formulario.save()
            return redirect("ficha_cliente", cliente_id=atendimento.cliente_id)
        marcar_campos_invalidos(formulario)
    else:
        formulario = AtendimentoForm()

    return render(
        request, "atendimentos/atendimento_form.html", {"formulario": formulario}
    )
