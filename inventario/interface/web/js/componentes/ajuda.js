import { esconderComTransicao, mostrarComTransicao } from "../animacoes.js";
import { criarElemento, gerarIdentificador } from "../elementos.js";
import { criarIcone } from "../icones.js";
import { posicionarJuntoDaAncora } from "../posicionamento.js";

const ESPERA_ANTES_DE_MOSTRAR = 250;

export function criarBotaoDeAjuda({ assunto, explicacao }) {
  const identificadorDaDica = gerarIdentificador("dica");
  const dica = criarElemento("div", {
    classe: "dica",
    role: "tooltip",
    id: identificadorDaDica,
    texto: explicacao,
  });
  const botao = criarElemento(
    "button",
    {
      type: "button",
      classe: "botao-de-ajuda",
      "aria-label": `O que é ${assunto}?`,
      "aria-describedby": identificadorDaDica,
    },
    [criarIcone("informacao")],
  );

  let temporizador = null;

  function mostrar() {
    clearTimeout(temporizador);
    if (dica.isConnected) {
      return;
    }
    document.body.append(dica);
    posicionarJuntoDaAncora(dica, botao, { lado: "acima", alinhamento: "centro" });
    mostrarComTransicao(dica);
  }

  function mostrarDepoisDeUmTempo() {
    clearTimeout(temporizador);
    temporizador = setTimeout(mostrar, ESPERA_ANTES_DE_MOSTRAR);
  }

  async function esconder() {
    clearTimeout(temporizador);
    if (!dica.isConnected || !dica.hasAttribute("data-visivel")) {
      return;
    }
    await esconderComTransicao(dica);
    if (!dica.hasAttribute("data-visivel")) {
      dica.remove();
    }
  }

  botao.addEventListener("pointerenter", (evento) => {
    if (evento.pointerType === "mouse") {
      mostrarDepoisDeUmTempo();
    }
  });
  botao.addEventListener("pointerleave", esconder);
  botao.addEventListener("focus", mostrar);
  botao.addEventListener("blur", esconder);
  botao.addEventListener("click", mostrar);
  botao.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && dica.isConnected) {
      evento.stopPropagation();
      esconder();
    }
  });

  return botao;
}
