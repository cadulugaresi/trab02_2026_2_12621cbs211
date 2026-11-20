import { listarRiscos } from "./api.js";

const CONFLITO_NOS_DADOS = 409;
const RISCOS_ZERADOS = { proprio: 0, herdado: 0, efetivo: 0 };

export async function buscarRiscosDoAtivo(idAtivo) {
  try {
    const ranking = await listarRiscos();
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
  } catch (erro) {
    if (erro.status === CONFLITO_NOS_DADOS) {
      return { valores: null, mensagem: erro.message };
    }
    throw erro;
  }
}
