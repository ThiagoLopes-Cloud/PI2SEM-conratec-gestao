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

5. Ligue o modo de desenvolvimento. Sem isso o Django entende que está em
   produção e exige a chave secreta em variável de ambiente.

   Windows (Prompt de Comando):

   ```
   set DJANGO_DEBUG=1
   ```

   Windows (PowerShell):

   ```
   $env:DJANGO_DEBUG = "1"
   ```

   Linux ou macOS:

   ```
   export DJANGO_DEBUG=1
   ```

   A variável vale enquanto o terminal estiver aberto. Em um terminal novo,
   defina de novo antes dos comandos seguintes.

6. Crie o banco de dados:

   ```
   python manage.py migrate
   ```

7. Carregue os dados de exemplo (opcional, mas recomendado para conhecer o
   sistema com o painel já preenchido):

   ```
   python manage.py seed
   ```

8. Suba o servidor:

   ```
   python manage.py runserver
   ```

9. Abra http://127.0.0.1:8000/ no navegador.

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
Várzea Paulista, seus equipamentos e atendimentos nos próximos dias. As datas
são contadas a partir do dia em que o comando roda, então o painel sempre tem o
que mostrar.

Cada execução refaz essa carga do zero: os 12 clientes fictícios e tudo que está
ligado a eles são apagados e criados de novo. Clientes cadastrados pelo sistema
não são afetados.

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

## Publicação

O projeto está preparado para rodar em servidor com SQLite e arquivos estáticos
servidos pelo WhiteNoise, sem depender de configuração de servidor web para o
CSS e o JavaScript.

### Variáveis de ambiente

| Variável                | Obrigatória            | O que faz |
| ----------------------- | ---------------------- | --------- |
| `DJANGO_SECRET_KEY`     | Sim, em produção       | Chave usada para assinar sessões e formulários. Em produção a aplicação se recusa a subir sem ela, com mensagem explicando o que falta. Em desenvolvimento, uma chave é sorteada a cada inicialização. Nunca deve ser escrita em arquivo do repositório. |
| `DJANGO_ALLOWED_HOSTS`  | Sim, em produção       | Endereços pelos quais o sistema aceita ser acessado, separados por vírgula, por exemplo `conratec.pythonanywhere.com`. Sem o endereço correto o Django recusa as requisições. O padrão é `127.0.0.1,localhost`. |
| `DJANGO_DEBUG`          | Não                    | `1` liga o modo de desenvolvimento: páginas de erro detalhadas e chave sorteada. Qualquer outro valor, ou a ausência da variável, deixa o sistema em modo de produção. Nunca ligar em servidor público. |

Com `DJANGO_DEBUG` desligado o sistema também passa a recusar conteúdo com tipo
declarado errado, bloquear exibição em quadro de outro site e exigir conexão
segura para os cookies de sessão e de formulário.

### Passos no servidor

```
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed
```

O `collectstatic` reúne o CSS e o JavaScript em `staticfiles/`, com nome
versionado e versão comprimida de cada arquivo. Precisa ser executado de novo a
cada alteração nesses arquivos. O `seed` só faz sentido em ambiente de
demonstração.

A geração de chave secreta pode ser feita com:

```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

O valor gerado vai na variável de ambiente do servidor, não em arquivo do
projeto.

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

**WhiteNoise.** Entrega os arquivos estáticos pela própria aplicação. Evita
configurar servidor web separado para o CSS e o JavaScript em uma hospedagem
simples, e serve os arquivos com nome versionado e comprimidos.

**API ViaCEP.** Preenche endereço, bairro e cidade a partir do CEP. Reduz erro de
digitação no dado que o painel usa para agrupar por região. É pública e não exige
cadastro nem chave de acesso.

## Acessibilidade

HTML semântico com um `h1` por página, `lang="pt-BR"`, label associada a todo
campo, link para pular ao conteúdo, contorno de foco visível e contraste de no
mínimo 4,5:1 entre texto e fundo.

## O que não está incluído

- Autenticação de usuários.
- Testes automatizados.

O sistema está configurado para publicação, mas ainda não há instância no ar.
