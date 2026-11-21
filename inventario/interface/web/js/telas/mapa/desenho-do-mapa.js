import { criarElementoSvg, gerarIdentificador } from "../../elementos.js";
import { formatarRisco } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { descobrirMaiorRisco } from "../../riscos.js";
import { iconeDoTipo } from "../ativos/apresentacao-do-ativo.js";
import { criarDefinicaoDaSeta } from "../ativos/mini-mapa.js";
import { ligacaoAparece } from "./ativos-visiveis.js";
import {
  calcularDiametro,
  descobrirPosicoesDosMaioresRiscos,
  indexarRankingPorId,
} from "./riscos-do-mapa.js";

const MARGENS_DO_MAPA = { lados: 64, topo: 44, base: 60 };
const MARGENS_DO_MAPA_ESTREITO = { lados: 44, topo: 40, base: 52 };
const RAIO_DA_MARCA_DE_MAIOR_RISCO = 9;
const RECUO_NA_ORIGEM = 2;
const RECUO_NO_DESTINO = 5;
const DISTANCIA_DO_ROTULO = 18;
const LIMITE_DO_ROTULO = 22;
const LIMITE_DO_ROTULO_ESTREITO = 16;
const SENO_DE_45_GRAUS = Math.SQRT1_2;

export function criarDesenhoDoMapa({
  ativos,
  ranking,
  posicoes,
  largura,
  altura,
  estreito = false,
  previa = false,
  buscados = new Set(),
}) {
  const margens = estreito ? MARGENS_DO_MAPA_ESTREITO : MARGENS_DO_MAPA;
  const limiteDoRotulo = estreito ? LIMITE_DO_ROTULO_ESTREITO : LIMITE_DO_ROTULO;
  const rankingPorId = indexarRankingPorId(ranking);
  const posicoesDosMaioresRiscos = descobrirPosicoesDosMaioresRiscos(ranking);
  const maiorRisco = descobrirMaiorRisco(ranking);
  const identificadorDaSeta = gerarIdentificador("seta-do-mapa");

  const desenho = criarElementoSvg("svg", {
    class: previa ? "mapa mapa-previa" : "mapa",
    viewBox: `0 0 ${largura} ${altura}`,
    width: String(largura),
    height: String(altura),
  });
  if (previa) {
    desenho.setAttribute("aria-hidden", "true");
  } else {
    desenho.setAttribute("role", "group");
    desenho.setAttribute("aria-label", "Mapa das dependências entre os ativos");
  }
  const camadaDasLigacoes = criarElementoSvg("g", { class: "mapa-ligacoes" });
  const camadaDosNos = criarElementoSvg("g", { class: "mapa-nos" });
  desenho.append(criarDefinicaoDaSeta(identificadorDaSeta), camadaDasLigacoes, camadaDosNos);

  const area = {
    esquerda: margens.lados,
    topo: margens.topo,
    largura: largura - 2 * margens.lados,
    altura: altura - margens.topo - margens.base,
  };
  const pontos = new Map();
  const raios = new Map();

  for (const ativo of ativos) {
    const fracao = posicoes.get(ativo.id);
    const ponto = {
      x: area.esquerda + fracao.x * area.largura,
      y: area.topo + fracao.y * area.altura,
    };
    const item = rankingPorId.get(ativo.id);
    const riscoEfetivo = item ? item.risco_efetivo : 0;
    const raio = calcularDiametro(riscoEfetivo, maiorRisco) / 2;
    const posicaoEntreOsMaiores = posicoesDosMaioresRiscos.get(ativo.id);
    const no = previa
      ? criarNoDaPrevia(raio, posicaoEntreOsMaiores)
      : criarNoDoMapa(ativo, item, raio, posicaoEntreOsMaiores, limiteDoRotulo);
    if (buscados.has(ativo.id)) {
      no.classList.add("mapa-no-buscado");
    }
    no.setAttribute("transform", `translate(${ponto.x} ${ponto.y})`);
    camadaDosNos.append(no);
    pontos.set(ativo.id, ponto);
    raios.set(ativo.id, raio);
  }

  for (const ativo of ativos) {
    for (const dependencia of ativo.dependencias) {
      const idDestino = dependencia.id_ativo_do_qual_depende;
      if (!pontos.has(idDestino) || !ligacaoAparece(ativo.id, idDestino, buscados)) {
        continue;
      }
      const linha = criarLigacao({
        origem: pontos.get(ativo.id),
        destino: pontos.get(idDestino),
        raioDaOrigem: raios.get(ativo.id),
        raioDoDestino: raios.get(idDestino),
      });
      if (linha === null) {
        continue;
      }
      linha.setAttribute("stroke-width", String(0.75 + dependencia.fracao * 2));
      if (!previa) {
        linha.setAttribute("marker-end", `url(#${identificadorDaSeta})`);
      }
      camadaDasLigacoes.append(linha);
    }
  }

  return desenho;
}

function criarLigacao({ origem, destino, raioDaOrigem, raioDoDestino }) {
  const distancia = Math.hypot(destino.x - origem.x, destino.y - origem.y);
  const recuoDaOrigem = raioDaOrigem + RECUO_NA_ORIGEM;
  const recuoDoDestino = raioDoDestino + RECUO_NO_DESTINO;
  if (distancia <= recuoDaOrigem + recuoDoDestino) {
    return null;
  }
  const direcaoX = (destino.x - origem.x) / distancia;
  const direcaoY = (destino.y - origem.y) / distancia;
  return criarElementoSvg("line", {
    class: "mapa-ligacao",
    x1: String(origem.x + direcaoX * recuoDaOrigem),
    y1: String(origem.y + direcaoY * recuoDaOrigem),
    x2: String(destino.x - direcaoX * recuoDoDestino),
    y2: String(destino.y - direcaoY * recuoDoDestino),
  });
}

function criarNoDoMapa(ativo, item, raio, posicaoEntreOsMaiores, limiteDoRotulo) {
  const tamanhoDoIcone = Math.round(raio * 0.9);
  const icone = criarIcone(iconeDoTipo(ativo.tipo), "mapa-icone");
  icone.setAttribute("x", String(-tamanhoDoIcone / 2));
  icone.setAttribute("y", String(-tamanhoDoIcone / 2));
  icone.setAttribute("width", String(tamanhoDoIcone));
  icone.setAttribute("height", String(tamanhoDoIcone));

  return criarElementoSvg(
    "a",
    {
      class: "mapa-no",
      href: `#/ativos/${ativo.id}`,
      "aria-label": descreverNo(ativo, item),
    },
    [
      criarElementoSvg("circle", { class: "mapa-no-fundo", r: String(raio) }),
      icone,
      criarMarcaDeMaiorRisco(raio, posicaoEntreOsMaiores),
      criarElementoSvg("text", {
        class: "mapa-rotulo",
        y: String(raio + DISTANCIA_DO_ROTULO),
        "text-anchor": "middle",
        texto: encurtarNome(ativo.nome, limiteDoRotulo),
      }),
    ],
  );
}

function criarNoDaPrevia(raio, posicaoEntreOsMaiores) {
  return criarElementoSvg("g", { class: "mapa-no" }, [
    criarElementoSvg("circle", { class: "mapa-no-fundo", r: String(raio) }),
    criarMarcaDeMaiorRisco(raio, posicaoEntreOsMaiores),
  ]);
}

function criarMarcaDeMaiorRisco(raio, posicaoEntreOsMaiores) {
  if (posicaoEntreOsMaiores === undefined) {
    return null;
  }
  const deslocamento = raio * SENO_DE_45_GRAUS;
  return criarElementoSvg(
    "g",
    {
      class: "mapa-marca-de-maior-risco",
      transform: `translate(${deslocamento} ${-deslocamento})`,
    },
    [
      criarElementoSvg("circle", { r: String(RAIO_DA_MARCA_DE_MAIOR_RISCO) }),
      criarElementoSvg("text", {
        "text-anchor": "middle",
        "dominant-baseline": "central",
        texto: String(posicaoEntreOsMaiores),
      }),
    ],
  );
}

function descreverNo(ativo, item) {
  if (item === undefined) {
    return ativo.nome;
  }
  return [
    ativo.nome,
    `${item.posicao}º no ranking`,
    `risco efetivo ${formatarRisco(item.risco_efetivo)}`,
  ].join(", ");
}

function encurtarNome(nome, limiteDoRotulo) {
  if (nome.length <= limiteDoRotulo) {
    return nome;
  }
  return `${nome.slice(0, limiteDoRotulo - 1)}…`;
}
