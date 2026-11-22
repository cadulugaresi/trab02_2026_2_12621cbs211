import { criarBotao } from "../../componentes/botoes.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarElemento } from "../../elementos.js";
import { buscarRanking, descobrirMaiorRisco } from "../../riscos.js";
import { navegarPara } from "../../roteador.js";
import { criarEstadoVazio, descreverQuantidade } from "../estados-da-lista.js";
import { criarLinhaDoRanking } from "./linha-do-ranking.js";

const QUANTIDADE_EM_DESTAQUE = 3;

export function montarTelaDeRanking(tela) {
  const contagem = criarElemento("p", {
    classe: "texto-de-apoio contagem-da-tela",
    "aria-live": "polite",
  });
  const faixa = criarFaixaDeErro();
  const destaques = criarElemento("ol", {
    classe: "ranking-destaques",
    "aria-label": "Os 3 maiores riscos",
  });
  const restante = criarElemento("ol", { classe: "ranking-restante", start: "4" });
  const areaDoRanking = criarElemento("div", { classe: "area-do-ranking", "aria-busy": "true" });
  const legenda = criarLegendaDoRanking();

  tela.append(criarCabecalhoDoRanking(contagem, legenda), faixa.elemento, areaDoRanking);

  async function carregar() {
    areaDoRanking.setAttribute("aria-busy", "true");
    try {
      const { ranking, mensagem } = await buscarRanking();
      faixa.esconder();
      if (ranking === null) {
        mostrarRankingIndisponivel(mensagem);
      } else {
        mostrarRanking(ranking);
      }
    } catch (erro) {
      faixa.mostrar(erro.message);
    } finally {
      areaDoRanking.removeAttribute("aria-busy");
    }
  }

  function mostrarRanking(ranking) {
    contagem.textContent = descreverQuantidade(ranking.length, "ativo", "ativos");
    legenda.hidden = ranking.length === 0;
    if (ranking.length === 0) {
      areaDoRanking.replaceChildren(
        criarElemento("ul", {}, [
          criarEstadoVazio({
            titulo: "Nenhum ativo no ranking",
            explicacao: "O ranking aparece quando houver ativos cadastrados.",
            textoDoBotao: "Cadastrar o primeiro ativo",
            aoClicar: () => navegarPara("/ativos/novo"),
          }),
        ]),
      );
      return;
    }
    const maiorRisco = descobrirMaiorRisco(ranking);
    destaques.replaceChildren();
    restante.replaceChildren();
    for (const [indice, item] of ranking.entries()) {
      const emDestaque = indice < QUANTIDADE_EM_DESTAQUE;
      const lista = emDestaque ? destaques : restante;
      lista.append(criarLinhaDoRanking(item, maiorRisco, emDestaque));
    }
    areaDoRanking.replaceChildren(destaques);
    if (restante.children.length > 0) {
      areaDoRanking.append(restante);
    }
  }

  function mostrarRankingIndisponivel(mensagem) {
    contagem.textContent = "";
    legenda.hidden = true;
    areaDoRanking.replaceChildren(
      criarElemento("div", { classe: "estado-vazio" }, [
        criarElemento("p", {
          classe: "estado-vazio-titulo",
          texto: "Não foi possível calcular o ranking",
        }),
        criarElemento("p", { classe: "texto-de-apoio", texto: mensagem }),
        criarBotao({ texto: "Tentar de novo", variacao: "secundario", aoClicar: carregar }),
      ]),
    );
  }

  carregar();
  return { atualizar: carregar };
}

function criarCabecalhoDoRanking(contagem, legenda) {
  return criarElemento("header", { classe: "cabecalho-de-tela cabecalho-com-acoes" }, [
    criarElemento("div", { classe: "cabecalho-de-tela-textos" }, [
      criarElemento("h1", { classe: "titulo-de-tela", texto: "Ranking de riscos" }),
      contagem,
    ]),
    legenda,
  ]);
}

function criarLegendaDoRanking() {
  return criarElemento("ul", { classe: "legenda-do-ranking", hidden: true }, [
    criarElemento("li", {}, [
      criarElemento("span", { classe: "amostra-da-barra amostra-propria" }),
      criarElemento("span", { texto: "Risco próprio" }),
    ]),
    criarElemento("li", {}, [
      criarElemento("span", { classe: "amostra-da-barra amostra-herdada" }),
      criarElemento("span", { texto: "Risco herdado" }),
    ]),
    criarElemento("li", { classe: "legenda-do-ranking-total", texto: "Número: risco efetivo" }),
  ]);
}
