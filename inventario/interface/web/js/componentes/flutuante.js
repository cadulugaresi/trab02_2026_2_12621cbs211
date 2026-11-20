import { esconderComTransicao, mostrarComTransicao } from "../animacoes.js";
import { abrirCamada, fecharCamada } from "../camadas.js";
import { criarElemento } from "../elementos.js";
import { posicionarJuntoDaAncora } from "../posicionamento.js";

export function abrirFlutuante({ conteudo, ancora, classe = "", preferencias = {}, aoFechar }) {
  const flutuante = criarElemento("div", { classe: `flutuante ${classe}`.trim() }, [conteudo]);
  document.body.append(flutuante);

  let estaFechado = false;
  const camada = {
    areasDeDentro: [flutuante, ancora],
    bloqueiaAPagina: false,
    pedirFechamento: () => fechar(),
  };

  function reposicionar() {
    posicionarJuntoDaAncora(flutuante, ancora, preferencias);
  }

  function fecharAoSairComTab(evento) {
    if (evento.key === "Tab") {
      fechar();
    }
  }

  async function fechar() {
    if (estaFechado) {
      return;
    }
    estaFechado = true;
    fecharCamada(camada);
    window.removeEventListener("resize", reposicionar);
    window.removeEventListener("scroll", reposicionar, true);
    ancora.setAttribute("aria-expanded", "false");
    if (flutuante.contains(document.activeElement)) {
      ancora.focus({ preventScroll: true });
    }
    if (aoFechar) {
      aoFechar();
    }
    await esconderComTransicao(flutuante);
    flutuante.remove();
  }

  reposicionar();
  abrirCamada(camada);
  ancora.setAttribute("aria-expanded", "true");
  flutuante.addEventListener("keydown", fecharAoSairComTab);
  window.addEventListener("resize", reposicionar);
  window.addEventListener("scroll", reposicionar, true);
  mostrarComTransicao(flutuante);

  return { elemento: flutuante, fechar, reposicionar };
}
