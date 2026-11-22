const TEMPO_LIMITE_DA_REQUISICAO = 10000;

let filaDeRequisicoes = Promise.resolve();

export function buscarNaFila(caminho, opcoes = {}) {
  const resultado = filaDeRequisicoes.then(() => buscarComTempoLimite(caminho, opcoes));
  filaDeRequisicoes = resultado.catch(() => {});
  return resultado;
}

export function ehErroDeDemora(erro) {
  return erro.name === "AbortError";
}

async function buscarComTempoLimite(caminho, opcoes) {
  const controlador = new AbortController();
  const temporizador = setTimeout(() => controlador.abort(), TEMPO_LIMITE_DA_REQUISICAO);
  try {
    return await fetch(caminho, { ...opcoes, signal: controlador.signal });
  } finally {
    clearTimeout(temporizador);
  }
}
