import { criarElemento, criarElementoSvg } from "../../elementos.js";

const LARGURA = 240;
const ALTURA = 128;
const CENTRO = { x: 120, y: 120 };
const RAIO = 108;
const ESPESSURA = 8;
const FOLGA_ENTRE_TRECHOS = 0.03;

export function criarMeiaLua({ vinculosPorStatus, totalDeVinculos, porcentagemDeCorrigidas }) {
  const desenho = criarElementoSvg(
    "svg",
    { class: "meia-lua-desenho", viewBox: `0 0 ${LARGURA} ${ALTURA}`, "aria-hidden": "true" },
    [criarArco(Math.PI, 0, "meia-lua-trilho")],
  );
  for (const trecho of calcularTrechos(vinculosPorStatus, totalDeVinculos)) {
    const arco = criarArco(trecho.inicio, trecho.fim, "meia-lua-trecho");
    arco.setAttribute("data-cor", trecho.cor);
    desenho.append(arco);
  }

  const textoDaPorcentagem =
    porcentagemDeCorrigidas === null ? "—" : `${porcentagemDeCorrigidas}%`;
  const textoDeApoio =
    totalDeVinculos === 0 ? "Nenhum vínculo ainda" : `corrigidas de ${totalDeVinculos} vínculos`;

  return criarElemento("figure", { classe: "meia-lua" }, [
    criarElemento("div", { classe: "meia-lua-grafico" }, [
      desenho,
      criarElemento("p", { classe: "meia-lua-centro" }, [
        criarElemento("span", { classe: "meia-lua-porcentagem", texto: textoDaPorcentagem }),
        criarElemento("span", { classe: "meia-lua-apoio", texto: textoDeApoio }),
      ]),
    ]),
    criarLegenda(vinculosPorStatus),
  ]);
}

function calcularTrechos(vinculosPorStatus, totalDeVinculos) {
  const trechos = [];
  if (totalDeVinculos === 0) {
    return trechos;
  }
  let quantidadeDeTrechos = 0;
  for (const contagem of vinculosPorStatus) {
    if (contagem.quantidade > 0) {
      quantidadeDeTrechos += 1;
    }
  }
  const folga = quantidadeDeTrechos > 1 ? FOLGA_ENTRE_TRECHOS : 0;
  let anguloAtual = Math.PI;
  for (const contagem of vinculosPorStatus) {
    if (contagem.quantidade === 0) {
      continue;
    }
    const tamanho = (contagem.quantidade / totalDeVinculos) * Math.PI;
    const inicio = anguloAtual;
    const fim = anguloAtual - tamanho;
    trechos.push({
      inicio: inicio === Math.PI ? inicio : inicio - folga / 2,
      fim: fim <= 0.000001 ? 0 : fim + folga / 2,
      cor: contagem.opcao.cor,
    });
    anguloAtual = fim;
  }
  return trechos;
}

function criarArco(anguloInicial, anguloFinal, classe) {
  const inicio = pontoNoArco(anguloInicial);
  const fim = pontoNoArco(anguloFinal);
  return criarElementoSvg("path", {
    class: classe,
    d: `M ${inicio.x} ${inicio.y} A ${RAIO} ${RAIO} 0 0 1 ${fim.x} ${fim.y}`,
    "stroke-width": String(ESPESSURA),
  });
}

function pontoNoArco(angulo) {
  return {
    x: CENTRO.x + RAIO * Math.cos(angulo),
    y: CENTRO.y - RAIO * Math.sin(angulo),
  };
}

function criarLegenda(vinculosPorStatus) {
  const itens = [];
  for (const contagem of vinculosPorStatus) {
    itens.push(
      criarElemento("li", { classe: "meia-lua-legenda-item" }, [
        criarElemento("span", { classe: "bolinha", "data-cor": contagem.opcao.cor }),
        criarElemento("span", { texto: contagem.opcao.rotulo }),
        criarElemento("span", {
          classe: "meia-lua-legenda-numero",
          texto: String(contagem.quantidade),
        }),
      ]),
    );
  }
  return criarElemento("ul", { classe: "meia-lua-legenda" }, itens);
}
