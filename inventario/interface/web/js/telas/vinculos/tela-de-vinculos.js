import {
  atualizarStatusDoVinculo,
  desvincularVulnerabilidade,
  listarAtivos,
  listarVulnerabilidades,
} from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarLinhaDeVinculo } from "../../componentes/linha-de-vinculo.js";
import { criarSegmentado } from "../../componentes/segmentado.js";
import { criarElemento } from "../../elementos.js";
import { formatarCvss } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { carregarOpcoes } from "../../opcoes.js";
import { iconeDoTipo } from "../ativos/apresentacao-do-ativo.js";
import { descreverQuantidade, mostrarEsqueletoNaLista } from "../estados-da-lista.js";
import { criarCriacaoDeVinculo } from "./criacao-de-vinculo.js";

export function montarTelaDeVinculos(tela, { busca }) {
  const idAtivoInicial = /^\d+$/.test(busca.get("ativo") ?? "") ? Number(busca.get("ativo")) : null;
  const faixa = criarFaixaDeErro();
  const contagem = criarElemento("p", { classe: "texto-de-apoio", "aria-live": "polite" });
  const areaDaCriacao = criarElemento("div", { classe: "area-da-criacao-de-vinculo" });
  const areaDosGrupos = criarElemento("ul", { classe: "grupos-de-vinculos" });
  let modo = "ativo";
  let dados = null;
  let criacao = null;

  const trocaDeModo = criarSegmentado({
    rotulo: "Agrupar vínculos",
    variacao: "troca-de-modo",
    valor: modo,
    opcoes: [
      { valor: "ativo", rotulo: "Por ativo" },
      { valor: "vulnerabilidade", rotulo: "Por vulnerabilidade" },
    ],
    aoMudar: (novoModo) => {
      modo = novoModo;
      mostrarGrupos();
    },
  });
  trocaDeModo.elemento.classList.add("troca-de-agrupamento");

  tela.append(
    criarElemento("header", { classe: "cabecalho-de-tela cabecalho-com-acoes" }, [
      criarElemento("div", { classe: "cabecalho-de-tela-textos" }, [
        criarElemento("h1", { classe: "titulo-de-tela", texto: "Vínculos" }),
        contagem,
      ]),
      trocaDeModo.elemento,
    ]),
    faixa.elemento,
    areaDaCriacao,
    areaDosGrupos,
  );
  mostrarEsqueletoNaLista(areaDosGrupos);

  async function recarregar() {
    try {
      const [opcoes, ativos, vulnerabilidades] = await Promise.all([
        carregarOpcoes(),
        listarAtivos(),
        listarVulnerabilidades(),
      ]);
      dados = { opcoes, ativos, vulnerabilidades };
      faixa.esconder();
      montarCriacaoSeAindaNaoExiste();
      criacao.atualizarItens(ativos, vulnerabilidades);
      mostrarGrupos();
    } catch (erro) {
      faixa.mostrar(erro.message);
      areaDosGrupos.replaceChildren();
    }
  }

  function montarCriacaoSeAindaNaoExiste() {
    if (criacao !== null) {
      return;
    }
    criacao = criarCriacaoDeVinculo({
      opcoes: dados.opcoes,
      idAtivoInicial: idAtivoInicial,
      aoVincular: recarregar,
      aoFalhar: (erro) => faixa.mostrar(erro.message),
    });
    areaDaCriacao.append(criacao.elemento);
  }

  function mostrarGrupos() {
    if (dados === null) {
      return;
    }
    const acoes = {
      opcoesDeStatus: dados.opcoes.statusDeTratamento,
      aoDesvincular: async (idAtivo, idVulnerabilidade) => {
        await desvincularVulnerabilidade(idAtivo, idVulnerabilidade);
        mostrarAvisoDeSucesso("Vulnerabilidade desvinculada");
        await recarregar();
      },
      aoFalhar: (erro) => faixa.mostrar(erro.message),
    };
    const grupos =
      modo === "ativo" ? agruparPorAtivo(dados, acoes) : agruparPorVulnerabilidade(dados, acoes);

    contagem.textContent = descreverQuantidade(contarVinculos(dados.ativos), "vínculo", "vínculos");
    areaDosGrupos.replaceChildren(...grupos);
    if (grupos.length === 0) {
      areaDosGrupos.append(criarEstadoSemVinculos());
    }
  }

  recarregar();
  return { atualizar: recarregar };
}

function agruparPorAtivo(dados, acoes) {
  const vulnerabilidadesPorId = indexarVulnerabilidades(dados.vulnerabilidades);
  const grupos = [];
  for (const ativo of dados.ativos) {
    if (ativo.vulnerabilidades.length === 0) {
      continue;
    }
    const vinculos = [];
    for (const vinculo of ativo.vulnerabilidades) {
      vinculos.push({ vinculo, vulnerabilidade: vulnerabilidadesPorId.get(vinculo.id_vulnerabilidade) });
    }
    vinculos.sort((primeiro, segundo) => segundo.vulnerabilidade.cvss - primeiro.vulnerabilidade.cvss);

    const linhas = [];
    for (const { vinculo, vulnerabilidade } of vinculos) {
      linhas.push(
        criarLinhaDeVinculo({
          nome: vulnerabilidade.nome_vulnerabilidade,
          cvss: vulnerabilidade.cvss,
          nivel: vulnerabilidade.nivel,
          enderecoDoNome: `/vulnerabilidades/${vulnerabilidade.id_vulnerabilidade}`,
          ...criarAcoesDoVinculo(ativo, vulnerabilidade, vinculo, acoes),
        }),
      );
    }
    grupos.push(
      criarGrupo({
        cabecalho: [
          criarIcone(iconeDoTipo(ativo.tipo)),
          criarElemento("a", { href: `#/ativos/${ativo.id}`, texto: ativo.nome }),
        ],
        detalhe: descreverQuantidade(vinculos.length, "vulnerabilidade", "vulnerabilidades"),
        linhas: linhas,
      }),
    );
  }
  return grupos;
}

function agruparPorVulnerabilidade(dados, acoes) {
  const vulnerabilidadesEmOrdem = [...dados.vulnerabilidades];
  vulnerabilidadesEmOrdem.sort((primeira, segunda) => segunda.cvss - primeira.cvss);
  const grupos = [];
  for (const vulnerabilidade of vulnerabilidadesEmOrdem) {
    const afetados = listarAtivosDaVulnerabilidade(dados.ativos, vulnerabilidade.id_vulnerabilidade);
    if (afetados.length === 0) {
      continue;
    }
    const linhas = [];
    for (const { ativo, vinculo } of afetados) {
      linhas.push(
        criarLinhaDeVinculo({
          nome: ativo.nome,
          iconeDoAtivo: iconeDoTipo(ativo.tipo),
          enderecoDoNome: `/ativos/${ativo.id}`,
          ...criarAcoesDoVinculo(ativo, vulnerabilidade, vinculo, acoes),
        }),
      );
    }
    grupos.push(
      criarGrupo({
        cabecalho: [
          criarElemento("span", { classe: "bolinha", "data-nivel": vulnerabilidade.nivel }),
          criarElemento("a", {
            href: `#/vulnerabilidades/${vulnerabilidade.id_vulnerabilidade}`,
            texto: vulnerabilidade.nome_vulnerabilidade,
          }),
        ],
        detalhe: `CVSS ${formatarCvss(vulnerabilidade.cvss)} · ${descreverQuantidade(
          afetados.length,
          "ativo",
          "ativos",
        )}`,
        linhas: linhas,
      }),
    );
  }
  return grupos;
}

function criarAcoesDoVinculo(ativo, vulnerabilidade, vinculo, acoes) {
  return {
    opcoesDeStatus: acoes.opcoesDeStatus,
    statusDeTratamento: vinculo.status_tratamento,
    perguntaDoDesvinculo: `Desvincular ${vulnerabilidade.nome_vulnerabilidade} de ${ativo.nome}?`,
    aoMudarStatus: async (novoStatus) => {
      await atualizarStatusDoVinculo(ativo.id, vinculo.id_vulnerabilidade, novoStatus);
      vinculo.status_tratamento = novoStatus;
    },
    aoDesvincular: () => acoes.aoDesvincular(ativo.id, vinculo.id_vulnerabilidade),
    aoFalhar: acoes.aoFalhar,
  };
}

function listarAtivosDaVulnerabilidade(ativos, idVulnerabilidade) {
  const afetados = [];
  for (const ativo of ativos) {
    for (const vinculo of ativo.vulnerabilidades) {
      if (vinculo.id_vulnerabilidade === idVulnerabilidade) {
        afetados.push({ ativo, vinculo });
      }
    }
  }
  afetados.sort((primeiro, segundo) => primeiro.ativo.nome.localeCompare(segundo.ativo.nome));
  return afetados;
}

function criarGrupo({ cabecalho, detalhe, linhas }) {
  return criarElemento("li", { classe: "grupo-de-vinculos" }, [
    criarElemento("div", { classe: "cabecalho-do-grupo" }, [
      criarElemento("h2", { classe: "cabecalho-do-grupo-titulo" }, cabecalho),
      criarElemento("span", { classe: "legenda", texto: detalhe }),
    ]),
    criarElemento("ul", {}, linhas),
  ]);
}

function criarEstadoSemVinculos() {
  return criarElemento("li", { classe: "estado-vazio" }, [
    criarElemento("p", { classe: "estado-vazio-titulo", texto: "Nenhum vínculo ainda" }),
    criarElemento("p", {
      classe: "texto-de-apoio",
      texto: "Escolha um ativo e uma vulnerabilidade acima e clique em Vincular.",
    }),
  ]);
}

function indexarVulnerabilidades(vulnerabilidades) {
  const vulnerabilidadesPorId = new Map();
  for (const vulnerabilidade of vulnerabilidades) {
    vulnerabilidadesPorId.set(vulnerabilidade.id_vulnerabilidade, vulnerabilidade);
  }
  return vulnerabilidadesPorId;
}

function contarVinculos(ativos) {
  let quantidade = 0;
  for (const ativo of ativos) {
    quantidade += ativo.vulnerabilidades.length;
  }
  return quantidade;
}
