const LARGURA_DO_CELULAR = 768;

const ALTURA_VISIVEL = 560;
const LADO_DO_ESPACO_DE_CADA_ATIVO_NO_COMPUTADOR = 190;
const LADO_DO_ESPACO_DE_CADA_ATIVO_NO_CELULAR = 150;
const LARGURA_DA_FAIXA_DE_NAVEGACAO = 72;
const MARGEM_DO_CONTEUDO_NO_COMPUTADOR = 64;
const MARGEM_DO_CONTEUDO_NO_CELULAR = 20;
const LARGURA_MAXIMA_DO_CONTEUDO = 1120;
const TELA_GRANDE = "(min-width: 1600px)";

export function medirMapa(larguraDaArea, quantidadeDeAtivos) {
  const ehCelular = larguraDaArea < LARGURA_DO_CELULAR;
  const visivel = { largura: Math.round(larguraDaArea), altura: ALTURA_VISIVEL };
  const ladoDoEspaco = ehCelular
    ? LADO_DO_ESPACO_DE_CADA_ATIVO_NO_CELULAR
    : LADO_DO_ESPACO_DE_CADA_ATIVO_NO_COMPUTADOR;
  const areaNecessaria = quantidadeDeAtivos * ladoDoEspaco * ladoDoEspaco;
  const areaVisivel = visivel.largura * visivel.altura;

  if (areaNecessaria <= areaVisivel) {
    return { ehCelular, visivel, desenho: { ...visivel } };
  }
  if (ehCelular) {
    return {
      ehCelular,
      visivel,
      desenho: { largura: Math.round(areaNecessaria / visivel.altura), altura: visivel.altura },
    };
  }
  const fator = Math.sqrt(areaNecessaria / areaVisivel);
  return {
    ehCelular,
    visivel,
    desenho: {
      largura: Math.round(visivel.largura * fator),
      altura: Math.round(visivel.altura * fator),
    },
  };
}

export function estimarLarguraDaAreaDoMapa() {
  const larguraDaJanela = document.documentElement.clientWidth;
  if (larguraDaJanela < LARGURA_DO_CELULAR) {
    return larguraDaJanela - 2 * MARGEM_DO_CONTEUDO_NO_CELULAR;
  }
  const larguraLivre =
    larguraDaJanela - LARGURA_DA_FAIXA_DE_NAVEGACAO - 2 * MARGEM_DO_CONTEUDO_NO_COMPUTADOR;
  if (window.matchMedia(TELA_GRANDE).matches) {
    return larguraLivre;
  }
  return Math.min(LARGURA_MAXIMA_DO_CONTEUDO, larguraLivre);
}

export function podeArrastar(medidas) {
  return (
    medidas.desenho.largura > medidas.visivel.largura ||
    medidas.desenho.altura > medidas.visivel.altura
  );
}
