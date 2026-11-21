import { listarAtivos } from "../../api.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarPilulaDeStatus } from "../../componentes/pilula-de-status.js";
import { criarSegmentado } from "../../componentes/segmentado.js";
import { criarElemento } from "../../elementos.js";
import { criarIcone } from "../../icones.js";
import { carregarOpcoes, encontrarOpcao } from "../../opcoes.js";
import { navegarPara } from "../../roteador.js";
import {
  criarEstadoVazio,
  descreverQuantidade,
  mostrarEsqueletoNaLista,
} from "../estados-da-lista.js";
import { descreverAtivo, iconeDoTipo } from "./apresentacao-do-ativo.js";
import { criarCabecalhoDeAtivos } from "./cabecalho-de-ativos.js";
import {
  criarFiltrosDeAtivos,
  criarGrupoDeFiltro,
  existeFiltroDeAtivos,
  lerFiltrosDeAtivos,
} from "./filtros-de-ativos.js";

const ESPERA_DA_BUSCA = 250;

export function montarTelaDeAtivos(tela) {
  const filtros = lerFiltrosDeAtivos();
  const estadoDaOrdenacao = { ordenar: "id" };
  const faixa = criarFaixaDeErro();
  const contagem = criarElemento("p", { classe: "texto-de-apoio", "aria-live": "polite" });
  const lista = criarElemento("ul", { classe: "lista-de-ativos", "aria-label": "Ativos" });
  const areaDosFiltros = criarElemento("div", { classe: "filtros-da-lista" });
  let opcoes = null;
  let numeroDaConsulta = 0;
  let temporizadorDaBusca = null;

  tela.append(
    criarCabecalhoDeAtivos({ modo: "lista", contagem: contagem }),
    faixa.elemento,
    areaDosFiltros,
    lista,
  );
  mostrarEsqueletoNaLista(lista);

  async function consultar() {
    if (opcoes === null) {
      return;
    }
    numeroDaConsulta += 1;
    const numeroDestaConsulta = numeroDaConsulta;
    lista.setAttribute("aria-busy", "true");
    try {
      const ativos = await listarAtivos({
        tipo: filtros.tipo,
        status: filtros.status,
        nome: filtros.nome.trim(),
        ordenar: estadoDaOrdenacao.ordenar,
      });
      if (numeroDestaConsulta !== numeroDaConsulta) {
        return;
      }
      faixa.esconder();
      mostrarAtivos(filtrarPorSetor(ativos, filtros.setor));
    } catch (erro) {
      if (numeroDestaConsulta === numeroDaConsulta) {
        faixa.mostrar(erro.message);
        lista.replaceChildren();
      }
    } finally {
      if (numeroDestaConsulta === numeroDaConsulta) {
        lista.removeAttribute("aria-busy");
      }
    }
  }

  function mostrarAtivos(ativos) {
    contagem.textContent = descreverContagem(ativos.length, existeFiltroDeAtivos(filtros));
    lista.replaceChildren();
    if (ativos.length === 0) {
      lista.append(criarEstadoDaListaVazia(existeFiltroDeAtivos(filtros), limparFiltros));
      return;
    }
    for (const ativo of ativos) {
      lista.append(criarLinhaDeAtivo(ativo, opcoes));
    }
  }

  function aoDigitarNaBusca() {
    clearTimeout(temporizadorDaBusca);
    temporizadorDaBusca = setTimeout(consultar, ESPERA_DA_BUSCA);
  }

  const controlesDosFiltros = { limpar: () => {} };
  function limparFiltros() {
    controlesDosFiltros.limpar();
    consultar();
  }

  carregarOpcoes()
    .then((opcoesCarregadas) => {
      opcoes = opcoesCarregadas;
      const filtrosMontados = criarFiltrosDeAtivos({
        opcoes: opcoes,
        filtros: filtros,
        textoDaBusca: "Buscar ativo por nome",
        aoMudar: consultar,
        aoDigitarNaBusca: aoDigitarNaBusca,
        gruposExtras: [criarOrdenacao(estadoDaOrdenacao, consultar)],
      });
      controlesDosFiltros.limpar = filtrosMontados.limpar;
      areaDosFiltros.append(filtrosMontados.elemento);
      consultar();
    })
    .catch((erro) => {
      faixa.mostrar(erro.message);
      lista.replaceChildren();
    });

  return {
    atualizar: consultar,
    desmontar: () => clearTimeout(temporizadorDaBusca),
  };
}

function criarOrdenacao(estadoDaOrdenacao, consultar) {
  const ordenacao = criarSegmentado({
    rotulo: "Ordenar por",
    valor: estadoDaOrdenacao.ordenar,
    opcoes: [
      { valor: "id", rotulo: "ID" },
      { valor: "nome", rotulo: "Nome" },
      { valor: "vulnerabilidades", rotulo: "Vulnerabilidades" },
    ],
    aoMudar: (valor) => {
      estadoDaOrdenacao.ordenar = valor;
      consultar();
    },
  });
  return criarGrupoDeFiltro("Ordenar por", ordenacao.elemento, "grupo-de-filtro-ordenacao");
}

function filtrarPorSetor(ativos, setor) {
  if (setor === null) {
    return ativos;
  }
  const ativosDoSetor = [];
  for (const ativo of ativos) {
    if (ativo.setor === setor) {
      ativosDoSetor.push(ativo);
    }
  }
  return ativosDoSetor;
}

function criarLinhaDeAtivo(ativo, opcoes) {
  const status = encontrarOpcao(opcoes.statusDoAtivo, ativo.status);
  const detalhes = `ID ${ativo.id} · ${descreverAtivo(ativo, opcoes)}`;
  const link = criarElemento("a", { classe: "linha-de-ativo", href: `#/ativos/${ativo.id}` }, [
    criarIcone(iconeDoTipo(ativo.tipo), "linha-de-ativo-icone"),
    criarElemento("span", { classe: "linha-de-ativo-textos" }, [
      criarElemento("span", { classe: "linha-de-ativo-nome", texto: ativo.nome }),
      criarElemento("span", { classe: "linha-de-ativo-detalhes", texto: detalhes }),
    ]),
    status ? criarPilulaDeStatus({ rotulo: status.rotulo, cor: status.cor }) : null,
    criarIcone("setaParaDireita", "linha-de-ativo-seta"),
  ]);
  return criarElemento("li", {}, [link]);
}

function criarEstadoDaListaVazia(comFiltros, limparFiltros) {
  if (comFiltros) {
    return criarEstadoVazio({
      titulo: "Nenhum ativo com esses filtros",
      explicacao: "Tente outro nome ou tire um dos filtros.",
      textoDoBotao: "Limpar filtros",
      variacao: "secundario",
      aoClicar: limparFiltros,
    });
  }
  return criarEstadoVazio({
    titulo: "Nenhum ativo cadastrado ainda",
    explicacao:
      "Cadastre notebooks, servidores, roteadores e impressoras para acompanhar o risco de cada um.",
    textoDoBotao: "Cadastrar o primeiro ativo",
    aoClicar: () => navegarPara("/ativos/novo"),
  });
}

function descreverContagem(quantidade, comFiltros) {
  if (comFiltros) {
    return descreverQuantidade(quantidade, "ativo encontrado", "ativos encontrados");
  }
  return descreverQuantidade(quantidade, "ativo", "ativos");
}
