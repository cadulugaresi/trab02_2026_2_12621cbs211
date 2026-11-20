import { criarElemento } from "../elementos.js";

export function criarNumeroAnimado({ valor, formatar, classe }) {
  const elemento = criarElemento("span", { classe: classe });
  let valorNaTela = valor;
  let quadroAgendado = null;

  function mostrar(novoValor) {
    valorNaTela = novoValor;
    elemento.textContent = formatar(novoValor);
  }

  function animarAte(valorFinal) {
    cancelAnimationFrame(quadroAgendado);
    const duracao = lerDuracaoDaContagem();
    if (duracao === 0) {
      mostrar(valorFinal);
      return;
    }

    const valorInicial = valorNaTela;
    const momentoInicial = performance.now();

    function desenharQuadro(agora) {
      const progresso = Math.min(1, (agora - momentoInicial) / duracao);
      mostrar(valorInicial + (valorFinal - valorInicial) * suavizarSaida(progresso));
      if (progresso < 1) {
        quadroAgendado = requestAnimationFrame(desenharQuadro);
      }
    }

    quadroAgendado = requestAnimationFrame(desenharQuadro);
  }

  mostrar(valor);
  return { elemento, animarAte };
}

function lerDuracaoDaContagem() {
  const textoDaDuracao = getComputedStyle(document.documentElement).getPropertyValue(
    "--duracao-da-contagem",
  );
  return parseFloat(textoDaDuracao) || 0;
}

function suavizarSaida(progresso) {
  return 1 - Math.pow(1 - progresso, 4);
}
