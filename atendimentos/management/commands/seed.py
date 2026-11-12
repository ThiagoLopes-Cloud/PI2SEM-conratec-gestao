from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from atendimentos.models import Atendimento, Cliente, Equipamento

CLIENTES = [
    {
        "nome": "Padaria Pão da Vila",
        "telefone": "(11) 94002-8911",
        "cep": "13220-110",
        "endereco": "Rua XV de Novembro, 284",
        "bairro": "Centro",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.COMERCIO,
        "observacoes": "Atender antes das 7h ou depois das 18h, fora do movimento.",
    },
    {
        "nome": "Marcos Aparecido Nunes",
        "telefone": "(11) 95511-3042",
        "cep": "13220-115",
        "endereco": "Rua São Benedito, 57",
        "bairro": "Centro",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.RESIDENCIA,
        "observacoes": "",
    },
    {
        "nome": "Drogaria Santa Rita",
        "telefone": "(11) 93388-7120",
        "cep": "13220-102",
        "endereco": "Avenida Fernando Arens, 1340",
        "bairro": "Centro",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.COMERCIO,
        "observacoes": "Nota fiscal em nome da matriz.",
    },
    {
        "nome": "Edifício Residencial Acácias",
        "telefone": "(11) 96140-5577",
        "cep": "13220-460",
        "endereco": "Rua das Acácias, 90",
        "bairro": "Jardim América",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.CONDOMINIO,
        "observacoes": "Falar com o zelador Osmar na portaria.",
    },
    {
        "nome": "Rosângela Pires de Almeida",
        "telefone": "(11) 94477-2308",
        "cep": "13220-455",
        "endereco": "Rua dos Jacarandás, 412",
        "bairro": "Jardim América",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.RESIDENCIA,
        "observacoes": "Cachorro solto no quintal.",
    },
    {
        "nome": "Oficina Mecânica Irmãos Prado",
        "telefone": "(11) 92233-6690",
        "cep": "13220-470",
        "endereco": "Rua Antônio Pinto, 1205",
        "bairro": "Jardim América",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.EMPRESA,
        "observacoes": "",
    },
    {
        "nome": "Escola Municipal Vila Real",
        "telefone": "(11) 91156-4402",
        "cep": "13223-220",
        "endereco": "Rua Projetada A, 15",
        "bairro": "Vila Real",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.PREDIO_PUBLICO,
        "observacoes": "Serviço só pode ser feito fora do horário de aula.",
    },
    {
        "nome": "Joel Ferreira da Costa",
        "telefone": "(11) 97705-1188",
        "cep": "13220-118",
        "endereco": "Rua Major Pinheiro, 76",
        "bairro": "Centro",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.RESIDENCIA,
        "observacoes": "",
    },
    {
        "nome": "Mercado Bom Preço",
        "telefone": "(11) 93012-7741",
        "cep": "13223-230",
        "endereco": "Avenida Vila Real, 820",
        "bairro": "Vila Real",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.COMERCIO,
        "observacoes": "Câmara fria é de outro fornecedor, não mexer.",
    },
    {
        "nome": "Benedita Soares Lima",
        "telefone": "(11) 95566-9023",
        "cep": "13225-340",
        "endereco": "Rua Paulistana, 338",
        "bairro": "Jd. Paulista",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.RESIDENCIA,
        "observacoes": "Só atende à tarde.",
    },
    {
        "nome": "Studio Pilates Corpo e Movimento",
        "telefone": "(11) 94890-3317",
        "cep": "13220-131",
        "endereco": "Rua Ipiranga, 61",
        "bairro": "Centro",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.COMERCIO,
        "observacoes": "",
    },
    {
        "nome": "Condomínio Portal do Sol",
        "telefone": "(11) 96602-4455",
        "cep": "13225-360",
        "endereco": "Rua das Palmeiras, 1500",
        "bairro": "Jd. Paulista",
        "cidade": "Várzea Paulista",
        "tipo": Cliente.Tipo.CONDOMINIO,
        "observacoes": "Salão de festas e academia têm split próprio.",
    },
]

EQUIPAMENTOS = [
    ("Padaria Pão da Vila", "Split Hi Wall Elgin Eco", 18000, "Salão de atendimento", -520),
    ("Padaria Pão da Vila", "Split Piso Teto Carrier", 36000, "Área de produção", -300),
    ("Marcos Aparecido Nunes", "Split Inverter LG Dual", 12000, "Quarto do casal", -210),
    ("Drogaria Santa Rita", "Split Hi Wall Samsung WindFree", 24000, "Loja", -640),
    ("Edifício Residencial Acácias", "Split Cassete Midea", 30000, "Salão de festas", -410),
    ("Rosângela Pires de Almeida", "Split Hi Wall Consul", 9000, "Sala de estar", -95),
    ("Oficina Mecânica Irmãos Prado", "Split Piso Teto Springer", 48000, "Recepção", -730),
    ("Escola Municipal Vila Real", "Split Hi Wall Gree", 18000, "Sala de informática", -365),
    ("Escola Municipal Vila Real", "Split Hi Wall Gree", 18000, "Secretaria", -365),
    ("Joel Ferreira da Costa", "Janela Consul Maxi", 10000, "Quarto dos fundos", -1100),
    ("Mercado Bom Preço", "Split Cassete Daikin", 36000, "Área de caixas", -250),
    ("Benedita Soares Lima", "Split Inverter Philco", 9000, "Sala", -150),
    ("Studio Pilates Corpo e Movimento", "Split Hi Wall TCL", 18000, "Sala de aula", -80),
    ("Condomínio Portal do Sol", "Split Hi Wall Agratto", 12000, "Academia", -480),
]

# cliente, local do equipamento, serviço, situação, dias a partir de hoje,
# valor e observações
ATENDIMENTOS = [
    (
        "Padaria Pão da Vila",
        "Área de produção",
        Atendimento.TipoServico.PREVENTIVA,
        Atendimento.Situacao.AGENDADO,
        0,
        "380.00",
        "Limpeza de filtros e checagem de gás.",
    ),
    (
        "Marcos Aparecido Nunes",
        "Quarto do casal",
        Atendimento.TipoServico.LIMPEZA,
        Atendimento.Situacao.AGENDADO,
        1,
        "160.00",
        "",
    ),
    (
        "Drogaria Santa Rita",
        "Loja",
        Atendimento.TipoServico.CORRETIVA,
        Atendimento.Situacao.ORCADO,
        1,
        "540.00",
        "Aparelho pingando água dentro da loja.",
    ),
    (
        "Rosângela Pires de Almeida",
        None,
        Atendimento.TipoServico.INSTALACAO,
        Atendimento.Situacao.ORCADO,
        2,
        "1250.00",
        "Split novo no quarto. O cliente já comprou o aparelho.",
    ),
    (
        "Edifício Residencial Acácias",
        "Salão de festas",
        Atendimento.TipoServico.PREVENTIVA,
        Atendimento.Situacao.AGENDADO,
        3,
        "420.00",
        "",
    ),
    (
        "Escola Municipal Vila Real",
        "Sala de informática",
        Atendimento.TipoServico.CORRETIVA,
        Atendimento.Situacao.AGENDADO,
        3,
        None,
        "Aparelho não liga. Ir depois das 17h.",
    ),
    (
        "Mercado Bom Preço",
        "Área de caixas",
        Atendimento.TipoServico.LIMPEZA,
        Atendimento.Situacao.A_ORCAR,
        4,
        None,
        "",
    ),
    (
        "Joel Ferreira da Costa",
        "Quarto dos fundos",
        Atendimento.TipoServico.CORRETIVA,
        Atendimento.Situacao.A_ORCAR,
        5,
        None,
        "Aparelho de janela fazendo barulho alto.",
    ),
    (
        "Benedita Soares Lima",
        "Sala",
        Atendimento.TipoServico.PREVENTIVA,
        Atendimento.Situacao.AGENDADO,
        6,
        "180.00",
        "Ligar antes. A cliente só atende à tarde.",
    ),
    (
        "Condomínio Portal do Sol",
        "Academia",
        Atendimento.TipoServico.PREVENTIVA,
        Atendimento.Situacao.ORCADO,
        7,
        "600.00",
        "",
    ),
    (
        "Studio Pilates Corpo e Movimento",
        "Sala de aula",
        Atendimento.TipoServico.LIMPEZA,
        Atendimento.Situacao.CONCLUIDO,
        -9,
        "220.00",
        "",
    ),
    (
        "Oficina Mecânica Irmãos Prado",
        "Recepção",
        Atendimento.TipoServico.CORRETIVA,
        Atendimento.Situacao.CONCLUIDO,
        -23,
        "760.00",
        "Troca da placa eletrônica.",
    ),
    # A padaria é cliente antiga e serve para demonstrar o histórico da ficha.
    (
        "Padaria Pão da Vila",
        "Salão de atendimento",
        Atendimento.TipoServico.LIMPEZA,
        Atendimento.Situacao.CONCLUIDO,
        -45,
        "150.00",
        "",
    ),
    (
        "Padaria Pão da Vila",
        "Área de produção",
        Atendimento.TipoServico.CORRETIVA,
        Atendimento.Situacao.CONCLUIDO,
        -118,
        "890.00",
        "Troca do capacitor da condensadora.",
    ),
    (
        "Padaria Pão da Vila",
        "Salão de atendimento",
        Atendimento.TipoServico.PREVENTIVA,
        Atendimento.Situacao.CONCLUIDO,
        -205,
        "380.00",
        "",
    ),
    (
        "Padaria Pão da Vila",
        "Área de produção",
        Atendimento.TipoServico.INSTALACAO,
        Atendimento.Situacao.CONCLUIDO,
        -300,
        "2400.00",
        "Instalação do piso teto na área de produção.",
    ),
]


class Command(BaseCommand):
    help = (
        "Recria os clientes, equipamentos e atendimentos fictícios de "
        "demonstração. Apaga e refaz esses registros; clientes cadastrados pelo "
        "sistema não são tocados."
    )

    def handle(self, *args, **opcoes):
        hoje = timezone.localdate()

        # As datas são contadas a partir do dia em que o comando roda, então a
        # carga é refeita do zero. Reaproveitar o que já existe faria o mesmo
        # atendimento entrar de novo a cada dia diferente.
        Cliente.objects.filter(nome__in=[dados["nome"] for dados in CLIENTES]).delete()

        clientes = {}
        for dados in CLIENTES:
            cliente = Cliente.objects.create(**dados)
            clientes[cliente.nome] = cliente

        equipamentos = {}
        for nome_cliente, modelo, btu, local, dias_desde_instalacao in EQUIPAMENTOS:
            equipamentos[(nome_cliente, local)] = Equipamento.objects.create(
                cliente=clientes[nome_cliente],
                modelo=modelo,
                capacidade_btu=btu,
                local_instalado=local,
                data_instalacao=hoje + timedelta(days=dias_desde_instalacao),
            )

        for nome_cliente, local, servico, situacao, dias, valor, observacoes in ATENDIMENTOS:
            Atendimento.objects.create(
                cliente=clientes[nome_cliente],
                equipamento=equipamentos.get((nome_cliente, local)),
                tipo_servico=servico,
                situacao=situacao,
                data_prevista=hoje + timedelta(days=dias),
                valor=valor,
                observacoes=observacoes,
            )

        # A data de cadastro é preenchida sozinha. Sem este ajuste todo cliente
        # apareceria como cadastrado hoje, com histórico anterior ao cadastro.
        for cliente in clientes.values():
            datas = [
                equipamento.data_instalacao
                for equipamento in cliente.equipamentos.all()
            ] + [
                atendimento.data_prevista for atendimento in cliente.atendimentos.all()
            ]
            if datas:
                cadastro = timezone.make_aware(datetime.combine(min(datas), time(9)))
                Cliente.objects.filter(pk=cliente.pk).update(criado_em=cadastro)

        self.stdout.write(
            "Dados de exemplo recriados. O banco tem agora "
            f"{Cliente.objects.count()} clientes, "
            f"{Equipamento.objects.count()} equipamentos e "
            f"{Atendimento.objects.count()} atendimentos."
        )
