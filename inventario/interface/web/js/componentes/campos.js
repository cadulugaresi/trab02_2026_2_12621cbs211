import { criarElemento, gerarIdentificador } from "../elementos.js";
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
