import { criarElemento } from "../elementos.js";
import { criarIcone } from "../icones.js";

const CLASSES_DAS_VARIACOES = {
  principal: "botao botao-principal",
  secundario: "botao botao-secundario",
  perigo: "botao botao-perigo",
  icone: "botao botao-icone",
  link: "botao botao-link",
};

export function criarBotao({
  texto,
  variacao = "principal",
  icone,
  iconeDepois,
  pequeno = false,
  rotuloAcessivel,
  aoClicar,
}) {
  const classes = `${CLASSES_DAS_VARIACOES[variacao]}${pequeno ? " botao-pequeno" : ""}`;
  const botao = criarElemento("button", {
    type: "button",
    classe: classes,
    "aria-label": rotuloAcessivel,
  });
  if (icone) {
    botao.append(criarIcone(icone));
  }
  if (texto) {
    botao.append(criarElemento("span", { texto: texto }));
  }
  if (iconeDepois) {
    botao.append(criarIcone(iconeDepois));
  }
  if (aoClicar) {
    botao.addEventListener("click", aoClicar);
  }
  return botao;
}

export function marcarBotaoComoOcupado(botao, textoEnquantoEspera) {
  const textoDoBotao = botao.querySelector("span");
  botao.dataset.textoOriginal = textoDoBotao ? textoDoBotao.textContent : "";
  botao.setAttribute("aria-busy", "true");
  botao.disabled = true;
  if (textoDoBotao) {
    textoDoBotao.textContent = textoEnquantoEspera;
  }
}

export function liberarBotao(botao) {
  const textoDoBotao = botao.querySelector("span");
  botao.removeAttribute("aria-busy");
  botao.disabled = false;
  if (textoDoBotao) {
    textoDoBotao.textContent = botao.dataset.textoOriginal;
  }
}
