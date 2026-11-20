const DISTANCIA_DA_ANCORA = 8;
const MARGEM_DA_TELA = 12;

export function posicionarJuntoDaAncora(flutuante, ancora, preferencias = {}) {
  const lado = preferencias.lado ?? "abaixo";
  const alinhamento = preferencias.alinhamento ?? "inicio";
  const caixaDaAncora = ancora.getBoundingClientRect();

  if (preferencias.mesmaLarguraDaAncora) {
    flutuante.style.minWidth = `${caixaDaAncora.width}px`;
  }

  const largura = flutuante.offsetWidth;
  const altura = flutuante.offsetHeight;
  const ladoFinal = escolherLado(lado, caixaDaAncora, altura);
  const topo = calcularTopo(ladoFinal, caixaDaAncora, altura);
  const esquerda = limitarNaTela(calcularEsquerda(alinhamento, caixaDaAncora, largura), largura);

  flutuante.style.top = `${topo}px`;
  flutuante.style.left = `${esquerda}px`;
  flutuante.style.transformOrigin = calcularOrigem(ladoFinal, caixaDaAncora, esquerda, altura);
}

function escolherLado(ladoPreferido, caixaDaAncora, altura) {
  const espacoAbaixo = window.innerHeight - caixaDaAncora.bottom - MARGEM_DA_TELA;
  const espacoAcima = caixaDaAncora.top - MARGEM_DA_TELA;
  const cabeAbaixo = altura + DISTANCIA_DA_ANCORA <= espacoAbaixo;
  const cabeAcima = altura + DISTANCIA_DA_ANCORA <= espacoAcima;

  if (ladoPreferido === "abaixo" && !cabeAbaixo && cabeAcima) {
    return "acima";
  }
  if (ladoPreferido === "acima" && !cabeAcima && cabeAbaixo) {
    return "abaixo";
  }
  return ladoPreferido;
}

function calcularTopo(lado, caixaDaAncora, altura) {
  if (lado === "acima") {
    return caixaDaAncora.top - DISTANCIA_DA_ANCORA - altura;
  }
  return caixaDaAncora.bottom + DISTANCIA_DA_ANCORA;
}

function calcularEsquerda(alinhamento, caixaDaAncora, largura) {
  if (alinhamento === "centro") {
    return caixaDaAncora.left + caixaDaAncora.width / 2 - largura / 2;
  }
  if (alinhamento === "fim") {
    return caixaDaAncora.right - largura;
  }
  return caixaDaAncora.left;
}

function limitarNaTela(esquerda, largura) {
  const maiorEsquerda = window.innerWidth - largura - MARGEM_DA_TELA;
  return Math.max(MARGEM_DA_TELA, Math.min(esquerda, maiorEsquerda));
}

function calcularOrigem(lado, caixaDaAncora, esquerda, altura) {
  const origemHorizontal = caixaDaAncora.left + caixaDaAncora.width / 2 - esquerda;
  const origemVertical = lado === "acima" ? altura : 0;
  return `${origemHorizontal}px ${origemVertical}px`;
}
