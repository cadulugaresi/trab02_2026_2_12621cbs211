export function validarTextoObrigatorio(erros, campo, texto) {
  const textoLimpo = texto.trim();
  if (textoLimpo === "") {
    erros.push({ campo, mensagem: "Este campo não pode ser vazio" });
  } else if (/^\d+$/.test(textoLimpo)) {
    erros.push({ campo, mensagem: "Este campo não pode ser composto apenas por números" });
  }
}

export function validarEscolha(erros, campo, valor) {
  if (valor === null) {
    erros.push({ campo, mensagem: "Escolha uma opção" });
  }
}

export function validarNumeroPositivo(erros, campo, numero) {
  if (numero === null || numero <= 0) {
    erros.push({ campo, mensagem: "Digite um número maior que zero" });
  }
}

export function validarInteiroPositivo(erros, campo, numero) {
  if (numero === null || numero <= 0) {
    erros.push({ campo, mensagem: "Digite um número inteiro maior que zero" });
  }
}

export function validarCvssPreenchido(erros, campo, cvss) {
  if (cvss === null) {
    erros.push({ campo, mensagem: "Digite o CVSS, de 0,1 a 10" });
  }
}
