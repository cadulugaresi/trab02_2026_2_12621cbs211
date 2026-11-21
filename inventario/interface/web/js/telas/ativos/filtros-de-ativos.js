import { criarPilulasDeFiltro } from "../../componentes/pilulas-de-filtro.js";
import { criarElemento } from "../../elementos.js";
import { normalizarParaBusca } from "../../formatos.js";
import { criarIcone } from "../../icones.js";

const filtrosCompartilhados = { tipo: null, status: null, setor: null, nome: "" };

export function lerFiltrosDeAtivos() {
  return filtrosCompartilhados;
}

export function existeFiltroDeAtivos(filtros) {
  return (
    filtros.tipo !== null ||
    filtros.status !== null ||
    filtros.setor !== null ||
    filtros.nome.trim() !== ""
  );
}

export function ativoPassaNosFiltros(ativo, filtros) {
  if (filtros.tipo !== null && ativo.tipo !== filtros.tipo) {
    return false;
  }
  if (filtros.status !== null && ativo.status !== filtros.status) {
    return false;
  }
  if (filtros.setor !== null && ativo.setor !== filtros.setor) {
    return false;
  }
  return true;
}

export function nomeCombinaComABusca(nome, textoDaBusca) {
  return normalizarParaBusca(nome).includes(normalizarParaBusca(textoDaBusca.trim()));
}

export function criarFiltrosDeAtivos({
  opcoes,
  filtros,
  textoDaBusca,
  aoMudar,
  aoDigitarNaBusca,
  gruposExtras = [],
}) {
  const busca = criarElemento("input", {
    type: "search",
    classe: "campo campo-de-busca",
    placeholder: textoDaBusca,
    "aria-label": textoDaBusca,
    autocomplete: "off",
    spellcheck: "false",
  });
  busca.value = filtros.nome;
  busca.addEventListener("input", () => {
    filtros.nome = busca.value;
    aoDigitarNaBusca();
  });

  const tipos = criarPilulasDeFiltro({
    rotulo: "Filtrar por tipo",
    variacao: "preenchida",
    opcoes: opcoes.tipos,
    valorInicial: filtros.tipo,
    aoMudar: (valor) => {
      filtros.tipo = valor;
      aoMudar();
    },
  });
  const status = criarPilulasDeFiltro({
    rotulo: "Filtrar por status",
    variacao: "contorno",
    opcoes: opcoes.statusDoAtivo,
    valorInicial: filtros.status,
    aoMudar: (valor) => {
      filtros.status = valor;
      aoMudar();
    },
  });
  const setores = criarPilulasDeFiltro({
    rotulo: "Filtrar por setor",
    variacao: "contorno",
    opcoes: opcoes.setores,
    valorInicial: filtros.setor,
    aoMudar: (valor) => {
      filtros.setor = valor;
      aoMudar();
    },
  });

  const elemento = criarElemento("div", { classe: "filtros-da-lista-conteudo" }, [
    criarElemento("div", { classe: "campo-de-busca-com-icone" }, [criarIcone("buscar"), busca]),
    criarElemento("div", { classe: "grupos-de-filtro" }, [
      criarGrupoDeFiltro("Tipo", tipos.elemento),
      criarGrupoDeFiltro("Status", status.elemento),
      criarGrupoDeFiltro("Setor", setores.elemento),
      ...gruposExtras,
    ]),
  ]);

  function limpar() {
    filtros.tipo = null;
    filtros.status = null;
    filtros.setor = null;
    filtros.nome = "";
    busca.value = "";
    tipos.limpar();
    status.limpar();
    setores.limpar();
  }

  return { elemento, limpar };
}

export function criarGrupoDeFiltro(titulo, controle, classeExtra = "") {
  return criarElemento("div", { classe: `grupo-de-filtro ${classeExtra}`.trim() }, [
    criarElemento("p", { classe: "legenda", texto: titulo }),
    controle,
  ]);
}
