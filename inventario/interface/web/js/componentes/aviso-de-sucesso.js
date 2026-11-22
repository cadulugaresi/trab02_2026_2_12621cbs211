import { esconderComTransicao, mostrarComTransicao } from "../animacoes.js";
import { criarElemento } from "../elementos.js";
import { criarIcone } from "../icones.js";

const TEMPO_NA_TELA = 3000;

let avisoNaTela = null;
let temporizadorDeSaida = null;

document.addEventListener("visibilitychange", () => {
  if (avisoNaTela === null) {
    return;
  }
  if (document.hidden) {
    clearTimeout(temporizadorDeSaida);
  } else {
    agendarSaida(avisoNaTela);
  }
});

export function mostrarAvisoDeSucesso(mensagem) {
  if (avisoNaTela !== null) {
    esconderAviso(avisoNaTela);
  }
  const aviso = criarElemento("div", { classe: "aviso-de-sucesso" }, [
    criarIcone("confirmado"),
    criarElemento("span", { texto: mensagem }),
  ]);
  document.getElementById("regiao-de-avisos").append(aviso);
  mostrarComTransicao(aviso);
  avisoNaTela = aviso;
  agendarSaida(aviso);
}

function agendarSaida(aviso) {
  clearTimeout(temporizadorDeSaida);
  temporizadorDeSaida = setTimeout(() => esconderAviso(aviso), TEMPO_NA_TELA);
}

async function esconderAviso(aviso) {
  if (avisoNaTela === aviso) {
    avisoNaTela = null;
    clearTimeout(temporizadorDeSaida);
  }
  await esconderComTransicao(aviso);
  aviso.remove();
}
