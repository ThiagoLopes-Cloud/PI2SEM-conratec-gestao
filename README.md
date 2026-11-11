# Conratec Gestão

Sistema web de gestão de atendimentos da Conratec, microempresa de instalação e
manutenção de ar-condicionado. Centraliza o cadastro de clientes, os
equipamentos instalados em cada endereço e os atendimentos previstos, e organiza
a agenda por região para reduzir deslocamento.

## O que o sistema faz

- **Painel** com os atendimentos dos próximos 7 dias, agrupados por bairro ou
  por data, com contagem em cada grupo e link direto para o endereço no Google
  Maps.
- **Distribuição dos clientes por bairro**, com barra proporcional, para mostrar
  onde a carteira está concentrada.
- **Ficha do cliente** com dados de contato, equipamentos instalados e histórico
  de atendimentos do mais recente para o mais antigo.
- **Cadastro de cliente** com preenchimento automático de endereço, bairro e
  cidade a partir do CEP.
- **Lançamento de atendimento** ligando cliente, equipamento, tipo de serviço,
  situação, data prevista e valor.

## Para quem é

Para o proprietário da Conratec, que atende sozinho e acumula as funções
técnicas e administrativas. O sistema tem um único usuário e roda na máquina
dele, por isso não há cadastro de usuários nem tela de login.

## Requisitos

- Python 3.10 ou mais recente.
- Acesso à internet enquanto o sistema estiver aberto: o Bootstrap vem de CDN e
  a busca de CEP consulta o ViaCEP. Sem internet o sistema continua funcionando,
  só perde o estilo visual e o preenchimento automático do endereço.
- Nenhum banco de dados a instalar. Os dados ficam em um arquivo SQLite criado
  na primeira execução.

## Como rodar

1. Clone o repositório e entre na pasta:

   ```
   git clone https://github.com/ThiagoLopes-Cloud/PI2SEM-conratec-gestao.git
   cd PI2SEM-conratec-gestao
   ```

2. Crie o ambiente virtual:

   ```
   python -m venv .venv
   ```

3. Ative o ambiente virtual.

   Windows:

   ```
   .venv\Scripts\activate
   ```

   Linux ou macOS:

   ```
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

5. Crie o banco de dados:

   ```
   python manage.py migrate
   ```

6. Carregue os dados de exemplo (opcional, mas recomendado para conhecer o
   sistema com o painel já preenchido):

   ```
   python manage.py seed
   ```

7. Suba o servidor:

   ```
   python manage.py runserver
   ```

8. Abra http://127.0.0.1:8000/ no navegador.

### Telas

| Endereço                 | Tela                      |
| ------------------------ | ------------------------- |
| `/`                      | Painel dos próximos 7 dias |
| `/clientes/novo/`        | Cadastro de cliente       |
| `/clientes/<id>/`        | Ficha do cliente          |
| `/atendimentos/novo/`    | Lançamento de atendimento |
| `/admin/`                | Administração do Django   |

O painel aceita `?agrupar=regiao` e `?agrupar=data` para alternar o agrupamento.

### Dados de exemplo

O comando `seed` cria 12 clientes fictícios distribuídos em quatro bairros de
Várzea Paulista, seus equipamentos e atendimentos nos próximos dias. Pode ser
executado mais de uma vez sem duplicar registros.

### Área administrativa

Para usar `/admin/`, crie um usuário:

```
python manage.py createsuperuser
```

## Estrutura de pastas

```
conratec-gestao/
├── conratec/                 configuração do projeto Django
│   ├── settings.py
│   └── urls.py
├── atendimentos/             aplicação com toda a regra de negócio
│   ├── models.py             Cliente, Equipamento e Atendimento
│   ├── views.py              painel, ficha e os dois formulários
│   ├── forms.py              ModelForms de cliente e atendimento
│   ├── admin.py
│   ├── urls.py
│   ├── migrations/
│   └── management/commands/
│       └── seed.py           carga de dados de exemplo
├── templates/
│   ├── base.html             cabeçalho, menu e link de pular conteúdo
│   └── atendimentos/         uma página por tela
├── static/
│   ├── css/conratec.css      estilos próprios sobre o Bootstrap
│   └── js/cep.js             consulta ao ViaCEP
├── Docs PI2SEM/              documentos da disciplina, fora da aplicação
├── manage.py
└── requirements.txt
```

## Tecnologias e por que foram escolhidas

**Django 5.2.** Entrega ORM, formulários validados, roteamento e área
administrativa sem código adicional. A administração pronta permitiu corrigir
dados durante o desenvolvimento antes que as telas existissem.

**SQLite.** O sistema tem um único usuário e roda em uma máquina só. Um banco em
arquivo evita instalar e manter um servidor de banco de dados para um volume de
onze a trinta atendimentos por mês.

**Bootstrap 5 via CDN.** Dá grade responsiva e componentes consistentes sem
introduzir etapa de build no projeto. As cores próprias ficam em
`static/css/conratec.css`, aplicadas sobre o Bootstrap.

**JavaScript sem bibliotecas.** O sistema tem um único comportamento dinâmico, a
busca de CEP. Uma biblioteca de interface custaria mais em dependência e tempo
de carga do que economizaria em código.

**API ViaCEP.** Preenche endereço, bairro e cidade a partir do CEP. Reduz erro de
digitação no dado que o painel usa para agrupar por região. É pública e não exige
cadastro nem chave de acesso.

## Acessibilidade

HTML semântico com um `h1` por página, `lang="pt-BR"`, label associada a todo
campo, link para pular ao conteúdo, contorno de foco visível e contraste de no
mínimo 4,5:1 entre texto e fundo.

## O que não está incluído

- Autenticação de usuários.
- Publicação em servidor. O projeto roda localmente.
- Testes automatizados.
