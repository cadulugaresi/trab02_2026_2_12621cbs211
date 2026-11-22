import { criarSegmentado } from "../../componentes/segmentado.js";
import { criarElemento } from "../../elementos.js";
import { navegarPara } from "../../roteador.js";

const ENDERECO_DE_CADA_MODO = {
  lista: "/ativos",
  mapa: "/ativos/mapa",
};

export function criarCabecalhoDeAtivos({ modo, contagem }) {
  const trocaDeModo = criarSegmentado({
    rotulo: "Modo de exibição",
    variacao: "troca-de-modo",
    valor: modo,
    opcoes: [
      { valor: "lista", rotulo: "Lista" },
      { valor: "mapa", rotulo: "Mapa" },
    ],
    aoMudar: (novoModo) => {
      if (novoModo !== modo) {
        navegarPara(ENDERECO_DE_CADA_MODO[novoModo]);
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
