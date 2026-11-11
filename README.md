# Conratec Gestão

Sistema web de gestão de atendimentos da Conratec, microempresa de instalação
e manutenção de ar-condicionado. Cadastra clientes e equipamentos, registra
atendimentos e mostra no painel o que está previsto para os próximos dias,
agrupado por região.

## Tecnologias

Django 5.2, SQLite, Bootstrap 5 (CDN) e JavaScript sem bibliotecas.

## Como rodar

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Aplicação em http://127.0.0.1:8000/.

No Linux ou macOS, troque a ativação do ambiente por `source .venv/bin/activate`.

O comando `seed` carrega clientes, equipamentos e atendimentos fictícios para
demonstração.

## Telas

- `/` painel de atendimentos dos próximos 7 dias
- `/clientes/<id>/` ficha do cliente
- `/clientes/novo/` cadastro de cliente
- `/atendimentos/novo/` lançamento de atendimento
