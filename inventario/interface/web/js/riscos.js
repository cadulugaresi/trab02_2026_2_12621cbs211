import { listarRiscos } from "./api.js";

const CONFLITO_NOS_DADOS = 409;
const RISCOS_ZERADOS = { proprio: 0, herdado: 0, efetivo: 0 };

export async function buscarRanking() {
  try {
    const ranking = await listarRiscos();
    return { ranking: ranking, mensagem: "" };
  } catch (erro) {
    if (erro.status === CONFLITO_NOS_DADOS) {
      return { ranking: null, mensagem: erro.message };
    }
    throw erro;
  }
}

export async function buscarRiscosDoAtivo(idAtivo) {
  const { ranking, mensagem } = await buscarRanking();
  if (ranking === null) {
    return { valores: null, mensagem: mensagem };
  }
  for (const posicao of ranking) {
    if (posicao.id === idAtivo) {
      return {
        valores: {
          proprio: posicao.risco_proprio,
          herdado: posicao.risco_herdado,
          efetivo: posicao.risco_efetivo,
        },
        mensagem: "",
      };
    }
  }
  return { valores: RISCOS_ZERADOS, mensagem: "" };
}

export function descobrirMaiorRisco(ranking) {
  let maiorRisco = 0;
  if (ranking === null) {
    return maiorRisco;
  }
  for (const item of ranking) {
    maiorRisco = Math.max(maiorRisco, item.risco_efetivo);
  }
  return maiorRisco;
}
