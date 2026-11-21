import { listarAtivos, listarVulnerabilidades } from "../../api.js";
import { criarBotao } from "../../componentes/botoes.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarElemento } from "../../elementos.js";
import { criarIcone } from "../../icones.js";
import { carregarOpcoes } from "../../opcoes.js";
import { buscarRanking, descobrirMaiorRisco } from "../../riscos.js";
import { navegarPara } from "../../roteador.js";
import { criarLinhaDoRanking } from "../ranking/linha-do-ranking.js";
import { criarBarrasDosSetores } from "./barras-dos-setores.js";
import { montarResumoDoInicio } from "./contas-do-inicio.js";
import { criarMeiaLua } from "./meia-lua.js";
import { criarPreviaDoMapa } from "./previa-do-mapa.js";

const NOME_DA_SAUDACAO = "Anakin";
const FUSO_HORARIO = "America/Sao_Paulo";
const QUANTIDADE_DE_URGENTES = 5;

export function montarTelaDeInicio(tela) {
  const faixa = criarFaixaDeErro();
  const frase = criarElemento("div", { classe: "frase-do-mais-urgente", "aria-live": "polite" }, [
    criarElemento("p", { classe: "texto-de-apoio", texto: "Carregando o resumo…" }),
  ]);
  const areaDaPrevia = criarElemento("div", { classe: "inicio-previa" });
  const areaDoResumo = criarElemento("div", { classe: "inicio-resumo", "aria-busy": "true" });

  tela.classList.add("tela-de-inicio");
  tela.append(
    criarElemento("header", { classe: "inicio-saudacao" }, [
      criarElemento("p", { classe: "inicio-data", texto: escreverDataDeHoje() }),
      criarElemento("h1", { classe: "saudacao", texto: escreverSaudacao() }),
      frase,
    ]),
    areaDaPrevia,
    faixa.elemento,
    areaDoResumo,
  );

  async function carregar() {
    try {
      const opcoes = await carregarOpcoes();
      const ativos = await listarAtivos();
      const vulnerabilidades = await listarVulnerabilidades();
      const { ranking, mensagem } = await buscarRanking();
      faixa.esconder();
      const resumo = montarResumoDoInicio({ ativos, vulnerabilidades, opcoes });
      frase.replaceChildren(...criarFrase(resumo.frase));
      areaDaPrevia.replaceChildren();
      if (ativos.length > 0) {
        areaDaPrevia.append(criarPreviaDoMapa({ ativos, ranking, mensagem }));
      }
      areaDoResumo.replaceChildren(
        criarFaixaDeNumeros(resumo.numeros),
        criarElemento("div", { classe: "inicio-graficos" }, [
          criarSecao("Tratamento dos vínculos", [criarMeiaLua(resumo)]),
          criarSecao("Críticas e altas abertas por setor", [
            criarBarrasDosSetores(resumo.setores),
          ]),
        ]),
        criarSecaoDosUrgentes(ranking, mensagem),
      );
    } catch (erro) {
      faixa.mostrar(erro.message);
      frase.replaceChildren();
    } finally {
      areaDoResumo.removeAttribute("aria-busy");
    }
  }

  carregar();
  return { atualizar: carregar };
}

function escreverSaudacao() {
  const hora = Number(
    new Intl.DateTimeFormat("pt-BR", {
      timeZone: FUSO_HORARIO,
      hour: "numeric",
      hourCycle: "h23",
    }).format(new Date()),
  );
  if (hora >= 5 && hora < 12) {
    return `Bom dia, ${NOME_DA_SAUDACAO}`;
  }
  if (hora >= 12 && hora < 18) {
    return `Boa tarde, ${NOME_DA_SAUDACAO}`;
  }
  return `Boa noite, ${NOME_DA_SAUDACAO}`;
}

function escreverDataDeHoje() {
  const data = new Intl.DateTimeFormat("pt-BR", {
    timeZone: FUSO_HORARIO,
    weekday: "long",
    day: "numeric",
    month: "long",
  }).format(new Date());
  return data.charAt(0).toUpperCase() + data.slice(1);
}

function criarFrase(frase) {
  const linhaPrincipal = criarElemento("p", { classe: "frase-principal" });
  if (frase.quantidade !== null) {
    linhaPrincipal.append(
      criarElemento("strong", { texto: String(frase.quantidade) }),
      ` ${frase.texto}`,
    );
  } else {
    linhaPrincipal.textContent = frase.texto;
  }
  const linhas = [linhaPrincipal];
  if (frase.complemento !== "") {
    linhas.push(criarElemento("p", { classe: "frase-complemento", texto: frase.complemento }));
  }
  return linhas;
}

function criarFaixaDeNumeros(numeros) {
  const itens = [
    { valor: numeros.ativos, singular: "ativo", plural: "ativos" },
    {
      valor: numeros.abertas,
      singular: "vulnerabilidade aberta",
      plural: "vulnerabilidades abertas",
    },
    { valor: numeros.criticasAbertas, singular: "crítica aberta", plural: "críticas abertas" },
    { valor: numeros.emManutencao, singular: "em manutenção", plural: "em manutenção" },
  ];
  const elementos = [];
  for (const item of itens) {
    elementos.push(
      criarElemento("li", { classe: "faixa-de-numeros-item" }, [
        criarElemento("span", { classe: "faixa-de-numeros-valor", texto: String(item.valor) }),
        criarElemento("span", {
          classe: "faixa-de-numeros-rotulo",
          texto: item.valor === 1 ? item.singular : item.plural,
        }),
      ]),
    );
  }
  return criarElemento("ul", { classe: "faixa-de-numeros" }, elementos);
}

function criarSecao(titulo, filhos, acao) {
  return criarElemento("section", { classe: "secao-do-inicio" }, [
    criarElemento("div", { classe: "secao-do-inicio-cabecalho" }, [
      criarElemento("h2", { classe: "titulo-de-secao", texto: titulo }),
      acao,
    ]),
    ...filhos,
  ]);
}

function criarSecaoDosUrgentes(ranking, mensagem) {
  const linkDoRanking = criarElemento("a", { classe: "botao botao-link", href: "#/ranking" }, [
    criarElemento("span", { texto: "Ver ranking" }),
    criarIcone("avancar"),
  ]);
  if (ranking === null) {
    return criarSecao(
      "Mais urgentes",
      [criarElemento("p", { classe: "texto-de-apoio", texto: mensagem })],
      linkDoRanking,
    );
  }
  if (ranking.length === 0) {
    return criarSecao("Mais urgentes", [
      criarElemento("div", { classe: "inicio-sem-ativos" }, [
        criarElemento("p", {
          classe: "texto-de-apoio",
          texto: "Cadastre o primeiro ativo para ver quem precisa de atenção.",
        }),
        criarBotao({
          texto: "Cadastrar ativo",
          variacao: "secundario",
          icone: "mais",
          aoClicar: () => navegarPara("/ativos/novo"),
        }),
      ]),
    ]);
  }
  const maiorRisco = descobrirMaiorRisco(ranking);
  const lista = criarElemento("ol", { classe: "ranking-restante inicio-urgentes" });
  for (const item of ranking.slice(0, QUANTIDADE_DE_URGENTES)) {
    lista.append(criarLinhaDoRanking(item, maiorRisco, false));
  }
  return criarSecao("Mais urgentes", [lista], linkDoRanking);
}
