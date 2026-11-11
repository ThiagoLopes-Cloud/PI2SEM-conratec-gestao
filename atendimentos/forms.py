from django import forms

from .models import Atendimento, Cliente, Equipamento


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nome",
            "telefone",
            "cep",
            "endereco",
            "bairro",
            "cidade",
            "tipo",
            "observacoes",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "(11) 90000-0000"}
            ),
            "cep": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "00000-000",
                    "inputmode": "numeric",
                }
            ),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        help_texts = {
            "cep": "Digite o CEP e saia do campo para preencher o endereço sozinho.",
            "observacoes": "Horário de atendimento, cuidados no local, quem receber na portaria.",
        }


class EquipamentoEscolha(forms.ModelChoiceField):
    # Sem o nome do cliente a lista fica cheia de aparelhos indistinguíveis.
    def label_from_instance(self, equipamento):
        return f"{equipamento.cliente.nome} - {equipamento}"


class AtendimentoForm(forms.ModelForm):
    equipamento = EquipamentoEscolha(
        queryset=Equipamento.objects.select_related("cliente"),
        required=False,
        label="Equipamento",
        empty_label="Nenhum equipamento específico",
        help_text="Deixe em branco para serviços que não são de um aparelho já instalado, como uma instalação nova.",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Atendimento
        fields = [
            "cliente",
            "equipamento",
            "tipo_servico",
            "situacao",
            "data_prevista",
            "valor",
            "observacoes",
        ]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "tipo_servico": forms.Select(attrs={"class": "form-select"}),
            "situacao": forms.Select(attrs={"class": "form-select"}),
            "data_prevista": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "valor": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "placeholder": "0,00"}
            ),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        help_texts = {
            "valor": "Deixe em branco enquanto o serviço ainda não foi orçado.",
        }

    def clean(self):
        dados = super().clean()
        cliente = dados.get("cliente")
        equipamento = dados.get("equipamento")

        if cliente and equipamento and equipamento.cliente_id != cliente.id:
            self.add_error(
                "equipamento",
                f"Esse equipamento é de {equipamento.cliente.nome}, não de {cliente.nome}.",
            )

        return dados
