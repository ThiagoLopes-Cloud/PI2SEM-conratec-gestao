const campoCep = document.getElementById("id_cep");
const aviso = document.getElementById("aviso-cep");

function mostrarAviso(texto, situacao) {
  aviso.textContent = texto;
  aviso.className = "mensagem-cep" + (situacao ? " mensagem-cep-" + situacao : "");
}

function preencherEndereco(endereco) {
  document.getElementById("id_endereco").value = endereco.logradouro || "";
  document.getElementById("id_bairro").value = endereco.bairro || "";
  document.getElementById("id_cidade").value = endereco.localidade || "";
}

async function buscarCep() {
  const digitos = campoCep.value.replace(/\D/g, "");

  if (digitos === "") {
    mostrarAviso("", null);
    return;
  }

  if (digitos.length !== 8) {
    mostrarAviso("O CEP precisa ter 8 números. Confira o que foi digitado.", "erro");
    return;
  }

  mostrarAviso("Procurando o endereço...", null);

  let endereco;
  try {
    const resposta = await fetch("https://viacep.com.br/ws/" + digitos + "/json/");
    if (!resposta.ok) {
      throw new Error("resposta " + resposta.status);
    }
    endereco = await resposta.json();
  } catch {
    mostrarAviso(
      "Não foi possível consultar o CEP agora. Verifique a internet ou preencha o endereço à mão.",
      "erro"
    );
    return;
  }

  if (endereco.erro) {
    mostrarAviso("CEP não encontrado. Confira o número ou preencha o endereço à mão.", "erro");
    return;
  }

  preencherEndereco(endereco);
  campoCep.value = endereco.cep;
  mostrarAviso("Endereço preenchido. Falta o número e o complemento.", "ok");
}

if (campoCep && aviso) {
  campoCep.addEventListener("blur", buscarCep);
}
