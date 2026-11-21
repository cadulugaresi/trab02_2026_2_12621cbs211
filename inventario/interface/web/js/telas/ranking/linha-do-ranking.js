import { criarElemento } from "../../elementos.js";
import { formatarRisco } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { iconeDoTipo } from "../ativos/apresentacao-do-ativo.js";

export function criarLinhaDoRanking(item, maiorRisco, emDestaque) {
  return criarElemento(
    "li",
    { classe: emDestaque ? "linha-do-ranking linha-do-ranking-destaque" : "linha-do-ranking" },
    [
      criarElemento("a", { classe: "linha-do-ranking-link", href: `#/ativos/${item.id}` }, [
        criarElemento("span", {
          classe: "linha-do-ranking-posicao",
          texto: String(item.posicao),
          "aria-label": `${item.posicao}º`,
        }),
        criarElemento("span", { classe: "linha-do-ranking-nome" }, [
          criarIcone(iconeDoTipo(item.tipo)),
          criarElemento("span", { texto: item.nome }),
        ]),
        criarBarraDeRisco(item, maiorRisco),
        criarElemento("span", {
          classe: "linha-do-ranking-valor",
          texto: formatarRisco(item.risco_efetivo),
        }),
      ]),
    ],
  );
}

function criarBarraDeRisco(item, maiorRisco) {
  return criarElemento("span", { classe: "barra-de-risco" }, [
    criarElemento("span", {
      classe: "barra-de-risco-propria",
      style: `width: ${calcularPorcentagem(item.risco_proprio, maiorRisco)}%`,
    }),
    criarElemento("span", {
      classe: "barra-de-risco-herdada",
      style: `width: ${calcularPorcentagem(item.risco_herdado, maiorRisco)}%`,
    }),
    criarElemento("span", {
      classe: "visualmente-oculto",
      texto: `Risco próprio ${formatarRisco(item.risco_proprio)}, herdado ${formatarRisco(
        item.risco_herdado,
      )}, efetivo`,
    }),
  ]);
}

function calcularPorcentagem(valor, maiorRisco) {
  if (maiorRisco <= 0) {
    return 0;
  }
  return Math.min((valor / maiorRisco) * 100, 100);
}
