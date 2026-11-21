import { criarElementoSvg, gerarIdentificador } from "../../elementos.js";
import { criarIcone } from "../../icones.js";
import { iconeDoTipo } from "./apresentacao-do-ativo.js";

const LARGURA = 560;
const ALTURA_POR_LINHA = 72;
const RAIO_DO_NO = 20;
const TAMANHO_DO_ICONE = 18;
const COLUNA_DOS_QUE_DEPENDEM = 90;
const COLUNA_DO_CENTRO = LARGURA / 2;
const COLUNA_DAS_DEPENDENCIAS = LARGURA - 90;
const LIMITE_DO_ROTULO = 18;
const ESPACO_DO_ULTIMO_ROTULO = 12;

export function criarMiniMapa({ ativoCentral, dependeDe, dependemDele }) {
  const quantidadeDeLinhas = Math.max(dependeDe.length, dependemDele.length, 1);
  const alturaDosNos = quantidadeDeLinhas * ALTURA_POR_LINHA;
  const centro = { x: COLUNA_DO_CENTRO, y: alturaDosNos / 2 };
  const vizinhosDaEsquerda = posicionarVizinhos(dependemDele, COLUNA_DOS_QUE_DEPENDEM, alturaDosNos);
  const vizinhosDaDireita = posicionarVizinhos(dependeDe, COLUNA_DAS_DEPENDENCIAS, alturaDosNos);
  const identificadorDaSeta = gerarIdentificador("seta");

  const mapa = criarElementoSvg("svg", {
    class: "mini-mapa",
    viewBox: `0 0 ${LARGURA} ${alturaDosNos + ESPACO_DO_ULTIMO_ROTULO}`,
    role: "img",
    "aria-label": `Mapa das dependências de ${ativoCentral.nome}`,
  });
  mapa.append(criarDefinicaoDaSeta(identificadorDaSeta));

  for (const vizinho of vizinhosDaEsquerda) {
    mapa.append(criarLigacao(vizinho.ponto, centro, vizinho.fracao, identificadorDaSeta));
  }
  for (const vizinho of vizinhosDaDireita) {
    mapa.append(criarLigacao(centro, vizinho.ponto, vizinho.fracao, identificadorDaSeta));
  }
  for (const vizinho of [...vizinhosDaEsquerda, ...vizinhosDaDireita]) {
    mapa.append(criarNoVizinho(vizinho.ativo, vizinho.ponto));
  }
  mapa.append(criarNoCentral(ativoCentral, centro));

  return mapa;
}

function posicionarVizinhos(vizinhos, coluna, alturaDosNos) {
  const vizinhosPosicionados = [];
  for (const [indice, vizinho] of vizinhos.entries()) {
    const linha = (alturaDosNos / vizinhos.length) * (indice + 0.5);
    vizinhosPosicionados.push({ ...vizinho, ponto: { x: coluna, y: linha } });
  }
  return vizinhosPosicionados;
}

export function criarDefinicaoDaSeta(identificador) {
  return criarElementoSvg("defs", {}, [
    criarElementoSvg(
      "marker",
      {
        id: identificador,
        viewBox: "0 0 10 10",
        refX: "9",
        refY: "5",
        markerWidth: "8",
        markerHeight: "8",
        markerUnits: "userSpaceOnUse",
        orient: "auto",
      },
      [criarElementoSvg("path", { d: "M1 1 L9 5 L1 9", class: "mini-mapa-ponta" })],
    ),
  ]);
}

function criarLigacao(origem, destino, fracao, identificadorDaSeta) {
  const distancia = Math.hypot(destino.x - origem.x, destino.y - origem.y);
  const recuo = RAIO_DO_NO + 4;
  const direcaoX = (destino.x - origem.x) / distancia;
  const direcaoY = (destino.y - origem.y) / distancia;
  return criarElementoSvg("line", {
    class: "mini-mapa-ligacao",
    x1: String(origem.x + direcaoX * recuo),
    y1: String(origem.y + direcaoY * recuo),
    x2: String(destino.x - direcaoX * recuo),
    y2: String(destino.y - direcaoY * recuo),
    "stroke-width": String(1 + fracao * 3),
    "marker-end": `url(#${identificadorDaSeta})`,
  });
}

function criarNoVizinho(ativo, ponto) {
  return criarElementoSvg(
    "a",
    { href: `#/ativos/${ativo.id}`, class: "mini-mapa-no", "aria-label": ativo.nome },
    [
      criarElementoSvg("circle", { cx: String(ponto.x), cy: String(ponto.y), r: String(RAIO_DO_NO) }),
      posicionarIcone(criarIcone(iconeDoTipo(ativo.tipo)), ponto),
      criarRotulo(ativo.nome, ponto),
    ],
  );
}

function criarNoCentral(ativo, ponto) {
  return criarElementoSvg("g", { class: "mini-mapa-no mini-mapa-no-central" }, [
    criarElementoSvg("circle", { cx: String(ponto.x), cy: String(ponto.y), r: String(RAIO_DO_NO) }),
    posicionarIcone(criarIcone(iconeDoTipo(ativo.tipo)), ponto),
    criarRotulo(ativo.nome, ponto),
  ]);
}

function posicionarIcone(icone, ponto) {
  icone.setAttribute("x", String(ponto.x - TAMANHO_DO_ICONE / 2));
  icone.setAttribute("y", String(ponto.y - TAMANHO_DO_ICONE / 2));
  icone.setAttribute("width", String(TAMANHO_DO_ICONE));
  icone.setAttribute("height", String(TAMANHO_DO_ICONE));
  icone.classList.add("mini-mapa-icone");
  return icone;
}

function criarRotulo(nome, ponto) {
  const nomeCurto = nome.length > LIMITE_DO_ROTULO ? `${nome.slice(0, LIMITE_DO_ROTULO - 1)}…` : nome;
  return criarElementoSvg("text", {
    class: "mini-mapa-rotulo",
    x: String(ponto.x),
    y: String(ponto.y + RAIO_DO_NO + 16),
    "text-anchor": "middle",
    texto: nomeCurto,
  });
}
