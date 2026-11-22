import { criarElemento, gerarIdentificador } from "../elementos.js";

export function criarControleDeslizante({ minimo, maximo, passo, valor, formatar, aoMudar }) {
  const entrada = criarElemento("input", {
    type: "range",
    classe: "controle-deslizante-entrada",
    id: gerarIdentificador("deslizante"),
    min: String(minimo),
    max: String(maximo),
    step: String(passo),
  });
  const numero = criarElemento("span", {
    classe: "controle-deslizante-numero",
    "aria-hidden": "true",
  });
  const elemento = criarElemento("div", { classe: "controle-deslizante" }, [entrada, numero]);

  function mostrarValor() {
    const valorAtual = Number(entrada.value);
    const minimoAtual = Number(entrada.min);
    const maximoAtual = Number(entrada.max);
    const amplitude = maximoAtual - minimoAtual;
    const porcentagem = amplitude > 0 ? ((valorAtual - minimoAtual) / amplitude) * 100 : 100;
    entrada.style.setProperty("--preenchimento", `${porcentagem}%`);
    numero.textContent = formatar(valorAtual);
    entrada.setAttribute("aria-valuetext", formatar(valorAtual));
  }

  function definirValor(novoValor) {
    entrada.value = String(novoValor);
    mostrarValor();
  }

  function definirMaximo(novoMaximo) {
    entrada.max = String(novoMaximo);
    mostrarValor();
  }

  entrada.addEventListener("input", () => {
    mostrarValor();
    if (aoMudar) {
      aoMudar(Number(entrada.value));
    }
  });

  definirValor(valor);
  return {
    elemento,
    campo: entrada,
    obterValor: () => Number(entrada.value),
    definirValor,
    definirMaximo,
  };
}
