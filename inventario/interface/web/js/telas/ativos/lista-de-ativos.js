import { listarAtivos } from "../../api.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarPilulaDeStatus } from "../../componentes/pilula-de-status.js";
import { criarPilulasDeFiltro } from "../../componentes/pilulas-de-filtro.js";
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

const ESPERA_DA_BUSCA = 250;

export function montarTelaDeAtivos(tela) {
  const filtros = { tipo: null, status: null, nome: "", ordenar: "id" };
  const faixa = criarFaixaDeErro();
  const contagem = criarElemento("p", { classe: "texto-de-apoio", "aria-live": "polite" });
  const lista = criarElemento("ul", { classe: "lista-de-ativos", "aria-label": "Ativos" });
  const areaDosFiltros = criarElemento("div", { classe: "filtros-da-lista" });
  let opcoes = null;
  let numeroDaConsulta = 0;
  let temporizadorDaBusca = null;

  tela.append(
    criarCabecalhoDaLista(contagem),
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
        ordenar: filtros.ordenar,
      });
      if (numeroDestaConsulta !== numeroDaConsulta) {
        return;
      }
      faixa.esconder();
      mostrarAtivos(ativos);
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
    contagem.textContent = descreverContagem(ativos.length, existeFiltroAtivo(filtros));
    lista.replaceChildren();
    if (ativos.length === 0) {
      lista.append(criarEstadoDaListaVazia(existeFiltroAtivo(filtros), limparFiltros));
      return;
    }
    for (const ativo of ativos) {
      lista.append(criarLinhaDeAtivo(ativo, opcoes));
    }
  }

  function aoDigitarNaBusca(texto) {
    filtros.nome = texto;
    clearTimeout(temporizadorDaBusca);
    temporizadorDaBusca = setTimeout(consultar, ESPERA_DA_BUSCA);
  }

  const controlesDosFiltros = { limpar: () => {} };
  function limparFiltros() {
    filtros.tipo = null;
    filtros.status = null;
    filtros.nome = "";
    controlesDosFiltros.limpar();
    consultar();
  }

  carregarOpcoes()
    .then((opcoesCarregadas) => {
      opcoes = opcoesCarregadas;
      const filtrosMontados = criarFiltros(opcoes, filtros, consultar, aoDigitarNaBusca);
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

function criarCabecalhoDaLista(contagem) {
  const trocaDeModo = criarSegmentado({
    rotulo: "Modo de exibição",
    variacao: "troca-de-modo",
    valor: "lista",
    opcoes: [
      { valor: "lista", rotulo: "Lista" },
      { valor: "mapa", rotulo: "Mapa" },
    ],
    aoMudar: (valor) => {
      if (valor === "mapa") {
        navegarPara("/ativos/mapa");
      }
    },
  });
  trocaDeModo.elemento.classList.add("troca-lista-mapa");

  return criarElemento("header", { classe: "cabecalho-de-tela cabecalho-com-acoes" }, [
    criarElemento("div", { classe: "cabecalho-de-tela-textos" }, [
      criarElemento("h1", { classe: "titulo-de-tela", texto: "Ativos" }),
      contagem,
    ]),
    trocaDeModo.elemento,
  ]);
}

function criarFiltros(opcoes, filtros, consultar, aoDigitarNaBusca) {
  const busca = criarElemento("input", {
    type: "search",
    classe: "campo campo-de-busca",
    placeholder: "Buscar por nome",
    "aria-label": "Buscar ativo por nome",
    autocomplete: "off",
    spellcheck: "false",
  });
  busca.addEventListener("input", () => aoDigitarNaBusca(busca.value));

  const tipos = criarPilulasDeFiltro({
    rotulo: "Filtrar por tipo",
    variacao: "preenchida",
    opcoes: opcoes.tipos,
    aoMudar: (valor) => {
      filtros.tipo = valor;
      consultar();
    },
  });
  const status = criarPilulasDeFiltro({
    rotulo: "Filtrar por status",
    variacao: "contorno",
    opcoes: opcoes.statusDoAtivo,
    aoMudar: (valor) => {
      filtros.status = valor;
      consultar();
    },
  });
  const ordenacao = criarSegmentado({
    rotulo: "Ordenar por",
    valor: "id",
    opcoes: [
      { valor: "id", rotulo: "ID" },
      { valor: "nome", rotulo: "Nome" },
      { valor: "vulnerabilidades", rotulo: "Vulnerabilidades" },
    ],
    aoMudar: (valor) => {
      filtros.ordenar = valor;
      consultar();
    },
  });

  const elemento = criarElemento("div", { classe: "filtros-da-lista-conteudo" }, [
    criarElemento("div", { classe: "campo-de-busca-com-icone" }, [criarIcone("buscar"), busca]),
    criarElemento("div", { classe: "grupos-de-filtro" }, [
      criarGrupoDeFiltro("Tipo", tipos.elemento),
      criarGrupoDeFiltro("Status", status.elemento),
      criarGrupoDeFiltro("Ordenar por", ordenacao.elemento, "grupo-de-filtro-ordenacao"),
    ]),
  ]);

  function limpar() {
    busca.value = "";
    tipos.limpar();
    status.limpar();
  }

  return { elemento, limpar };
}

function criarGrupoDeFiltro(titulo, controle, classeExtra = "") {
  return criarElemento("div", { classe: `grupo-de-filtro ${classeExtra}`.trim() }, [
    criarElemento("p", { classe: "legenda", texto: titulo }),
    controle,
  ]);
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

function existeFiltroAtivo(filtros) {
  return filtros.tipo !== null || filtros.status !== null || filtros.nome.trim() !== "";
}

function descreverContagem(quantidade, comFiltros) {
  if (comFiltros) {
    return descreverQuantidade(quantidade, "ativo encontrado", "ativos encontrados");
  }
  return descreverQuantidade(quantidade, "ativo", "ativos");
}
