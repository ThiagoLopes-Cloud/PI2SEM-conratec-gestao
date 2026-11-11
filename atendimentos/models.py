from urllib.parse import quote_plus

from django.db import models


class Cliente(models.Model):
    class Tipo(models.TextChoices):
        RESIDENCIA = "residencia", "Residência"
        COMERCIO = "comercio", "Comércio"
        CONDOMINIO = "condominio", "Condomínio"
        EMPRESA = "empresa", "Empresa"
        PREDIO_PUBLICO = "predio_publico", "Prédio público"

    nome = models.CharField("nome", max_length=120)
    telefone = models.CharField("telefone", max_length=20)
    cep = models.CharField("CEP", max_length=9)
    endereco = models.CharField("endereço", max_length=160)
    bairro = models.CharField("bairro", max_length=80)
    cidade = models.CharField("cidade", max_length=80)
    tipo = models.CharField("tipo de imóvel", max_length=20, choices=Tipo.choices)
    observacoes = models.TextField("observações", blank=True)
    criado_em = models.DateTimeField("cadastrado em", auto_now_add=True)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def endereco_completo(self):
        return f"{self.endereco} - {self.bairro}, {self.cidade}"

    @property
    def url_maps(self):
        return (
            "https://www.google.com/maps/search/?api=1&query="
            + quote_plus(self.endereco_completo)
        )


class Equipamento(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        related_name="equipamentos",
        on_delete=models.CASCADE,
        verbose_name="cliente",
    )
    modelo = models.CharField("modelo", max_length=120)
    capacidade_btu = models.PositiveIntegerField("capacidade (BTU)")
    local_instalado = models.CharField("local instalado", max_length=120)
    data_instalacao = models.DateField("data da instalação")

    class Meta:
        verbose_name = "equipamento"
        verbose_name_plural = "equipamentos"
        ordering = ["cliente__nome", "local_instalado"]

    def __str__(self):
        return f"{self.modelo} {self.capacidade_btu} BTU - {self.local_instalado}"


class Atendimento(models.Model):
    class TipoServico(models.TextChoices):
        INSTALACAO = "instalacao", "Instalação"
        PREVENTIVA = "preventiva", "Manutenção preventiva"
        CORRETIVA = "corretiva", "Manutenção corretiva"
        LIMPEZA = "limpeza", "Limpeza"

    class Situacao(models.TextChoices):
        A_ORCAR = "a_orcar", "A orçar"
        ORCADO = "orcado", "Orçado"
        AGENDADO = "agendado", "Agendado"
        CONCLUIDO = "concluido", "Concluído"

    cliente = models.ForeignKey(
        Cliente,
        related_name="atendimentos",
        on_delete=models.CASCADE,
        verbose_name="cliente",
    )
    equipamento = models.ForeignKey(
        Equipamento,
        related_name="atendimentos",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="equipamento",
    )
    tipo_servico = models.CharField(
        "tipo de serviço", max_length=20, choices=TipoServico.choices
    )
    situacao = models.CharField(
        "situação",
        max_length=20,
        choices=Situacao.choices,
        default=Situacao.A_ORCAR,
    )
    data_prevista = models.DateField("data prevista")
    valor = models.DecimalField(
        "valor", max_digits=10, decimal_places=2, null=True, blank=True
    )
    observacoes = models.TextField("observações", blank=True)

    class Meta:
        verbose_name = "atendimento"
        verbose_name_plural = "atendimentos"
        ordering = ["data_prevista"]

    def __str__(self):
        return f"{self.get_tipo_servico_display()} - {self.cliente.nome}"
