import { criarElemento, gerarIdentificador } from "../elementos.js";
import { lerNumeroDigitado } from "../formatos.js";
import { criarBotaoDeAjuda } from "./ajuda.js";

export function criarCampoDeTexto({
  nome,
  valor = "",
  textoDeExemplo,
  obrigatorio = false,
  tamanhoMaximo,
}) {
  const campo = criarElemento("input", {
    type: "text",
    classe: "campo",
    id: gerarIdentificador("campo"),
    name: nome,
    placeholder: textoDeExemplo,
    required: obrigatorio,
    maxlength: tamanhoMaximo,
    autocomplete: "off",
  });
  campo.value = valor;
  return campo;
}

export function criarCampoDeNumero({ nome, valor = null, unidade, inteiro = false, textoDeExemplo }) {
  const campo = criarElemento("input", {
    type: "text",
    classe: "campo campo-de-numero",
    id: gerarIdentificador("numero"),
    name: nome,
    inputmode: inteiro ? "numeric" : "decimal",
    placeholder: textoDeExemplo,
    autocomplete: "off",
    maxlength: "15",
  });
  const elemento = unidade
    ? criarElemento("div", { classe: "campo-com-unidade" }, [
        campo,
        criarElemento("span", { classe: "unidade-do-campo", texto: unidade }),
      ])
    : campo;

  function definirValor(novoValor) {
    campo.value = novoValor === null ? "" : String(novoValor).replace(".", ",");
  }

  function obterValor() {
    const numero = lerNumeroDigitado(campo.value);
    if (numero === null || (inteiro && !Number.isInteger(numero))) {
      return null;
    }
    return numero;
  }

  campo.addEventListener("input", () => {
    const caracteresAceitos = inteiro ? /\D/g : /[^\d.,]/g;
    campo.value = campo.value.replace(caracteresAceitos, "");
  });

  definirValor(valor);
  return { elemento, campo, obterValor, definirValor };
}

export function criarLinhaDeCampo({
  rotulo,
  controle,
  alvoDoRotulo = controle,
  ajuda = "",
  explicacaoDoConceito,
}) {
  const textoDeAjuda = criarElemento("p", {
    classe: "ajuda-de-campo",
    id: gerarIdentificador("ajuda"),
    texto: ajuda,
    hidden: ajuda === "",
  });
  alvoDoRotulo.setAttribute("aria-describedby", textoDeAjuda.id);

  const linha = criarElemento("div", { classe: "linha-de-campo" }, [
    criarCabecalhoDoCampo(rotulo, alvoDoRotulo, explicacaoDoConceito),
    controle,
    textoDeAjuda,
  ]);
  return { elemento: linha, textoDeAjuda };
}

export function mostrarAjuda(textoDeAjuda, mensagem, ehErro = false) {
  textoDeAjuda.textContent = mensagem;
  textoDeAjuda.hidden = mensagem === "";
  textoDeAjuda.toggleAttribute("data-erro", ehErro);
}

function criarCabecalhoDoCampo(rotulo, alvoDoRotulo, explicacaoDoConceito) {
  const etiqueta = criarElemento("label", { for: alvoDoRotulo.id, texto: rotulo });
  if (!explicacaoDoConceito) {
    etiqueta.className = "rotulo-de-campo";
    return etiqueta;
  }
  return criarElemento("div", { classe: "rotulo-de-campo" }, [
    etiqueta,
    criarBotaoDeAjuda({ assunto: rotulo, explicacao: explicacaoDoConceito }),
  ]);
}
