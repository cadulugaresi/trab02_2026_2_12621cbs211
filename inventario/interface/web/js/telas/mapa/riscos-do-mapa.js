const DIAMETRO_MINIMO = 36;
const DIAMETRO_MAXIMO = 64;
export const QUANTIDADE_DE_MAIORES_RISCOS = 3;

export function indexarRankingPorId(ranking) {
  const rankingPorId = new Map();
  if (ranking === null) {
    return rankingPorId;
  }
  for (const item of ranking) {
    rankingPorId.set(item.id, item);
  }
  return rankingPorId;
}

export function descobrirPosicoesDosMaioresRiscos(ranking) {
  const posicoes = new Map();
  if (ranking === null) {
    return posicoes;
  }
  for (const item of ranking) {
    if (item.posicao <= QUANTIDADE_DE_MAIORES_RISCOS && item.risco_efetivo > 0) {
      posicoes.set(item.id, item.posicao);
    }
  }
  return posicoes;
}

export function calcularDiametro(riscoEfetivo, maiorRisco) {
  if (maiorRisco <= 0) {
    return DIAMETRO_MINIMO;
  }
  return DIAMETRO_MINIMO + (riscoEfetivo / maiorRisco) * (DIAMETRO_MAXIMO - DIAMETRO_MINIMO);
}
