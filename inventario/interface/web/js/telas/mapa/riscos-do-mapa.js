export const DIAMETRO_MINIMO = 36;
export const DIAMETRO_MAXIMO = 64;

export const TERCOS_DO_RANKING = {
  vermelho: "Terço de maior risco",
  amarelo: "Terço do meio",
  verde: "Terço de menor risco",
};

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

export function calcularCoresDasNotificacoes(ranking) {
  const cores = new Map();
  if (ranking === null) {
    return cores;
  }
  const quantidade = ranking.length;
  const ultimaPosicaoVermelha = Math.ceil(quantidade / 3);
  const ultimaPosicaoAmarela = Math.ceil((2 * quantidade) / 3);
  let riscoAnterior = null;
  let corAnterior = null;

  for (const item of ranking) {
    let cor = escolherCorPelaPosicao(item.posicao, ultimaPosicaoVermelha, ultimaPosicaoAmarela);
    if (item.risco_efetivo === riscoAnterior) {
      cor = corAnterior;
    }
    riscoAnterior = item.risco_efetivo;
    corAnterior = cor;
    cores.set(item.id, item.risco_efetivo === 0 ? "verde" : cor);
  }
  return cores;
}

export function calcularDiametro(riscoEfetivo, maiorRisco) {
  if (maiorRisco <= 0) {
    return DIAMETRO_MINIMO;
  }
  return DIAMETRO_MINIMO + (riscoEfetivo / maiorRisco) * (DIAMETRO_MAXIMO - DIAMETRO_MINIMO);
}

function escolherCorPelaPosicao(posicao, ultimaPosicaoVermelha, ultimaPosicaoAmarela) {
  if (posicao <= ultimaPosicaoVermelha) {
    return "vermelho";
  }
  if (posicao <= ultimaPosicaoAmarela) {
    return "amarelo";
  }
  return "verde";
}
