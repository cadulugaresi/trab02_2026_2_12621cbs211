import { criarElemento } from "../../elementos.js";
import { criarIcone } from "../../icones.js";
import { navegarPara } from "../../roteador.js";
import { criarDesenhoDoMapa } from "../mapa/desenho-do-mapa.js";
import { entregarMapaPuxado } from "../mapa/mapa-puxado.js";
import { estimarLarguraDaAreaDoMapa, medirMapa } from "../mapa/medidas-do-mapa.js";
import { calcularPosicoesDoMapa } from "../mapa/posicoes-do-mapa.js";

const ESCALA_DA_PREVIA = 0.8;

export function criarPreviaDoMapa({ ativos, ranking, mensagem }) {
  const medidas = medirMapa(estimarLarguraDaAreaDoMapa(), ativos.length);
  const { largura, altura } = medidas.desenho;
  const desenho = criarDesenhoDoMapa({
    ativos,
    ranking,
    posicoes: calcularPosicoesDoMapa(ativos, largura / altura),
    largura: largura,
    altura: altura,
    estreito: medidas.ehCelular,
    previa: true,
  });
  desenho.setAttribute("width", String(Math.round(largura * ESCALA_DA_PREVIA)));
  desenho.setAttribute("height", String(Math.round(altura * ESCALA_DA_PREVIA)));

  const previa = criarElemento(
    "a",
    { classe: "previa-do-mapa", href: "#/ativos/mapa", "aria-label": "Abrir o mapa dos ativos" },
    [
      desenho,
      criarElemento("span", { classe: "previa-do-mapa-legenda" }, [
        criarElemento("span", { texto: "Abrir o mapa" }),
        criarIcone("avancar"),
      ]),
    ],
  );

  previa.addEventListener("click", (evento) => {
    if (evento.metaKey || evento.ctrlKey || evento.shiftKey || evento.button !== 0) {
      return;
    }
    evento.preventDefault();
    entregarMapaPuxado({
      ativos,
      ranking,
      mensagem,
      retangulo: desenho.getBoundingClientRect(),
    });
    navegarPara("/ativos/mapa");
  });

  return previa;
}
