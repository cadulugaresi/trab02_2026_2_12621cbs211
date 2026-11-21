import { criarElemento } from "../elementos.js";
import { criarIcone } from "../icones.js";

export function criarPilulasDeFiltro({
  rotulo,
  opcoes,
  variacao = "preenchida",
  valorInicial = null,
  aoMudar,
}) {
  let valorEscolhido = null;
  const pilulas = [];
  const elemento = criarElemento("div", {
    classe: `pilulas-de-filtro pilulas-de-filtro-${variacao}`,
    role: "group",
    "aria-label": rotulo,
  });

  for (const opcao of opcoes) {
    const pilula = criarElemento("button", {
      type: "button",
      classe: "pilula-de-filtro",
      "aria-pressed": "false",
    });
    if (opcao.icone) {
      pilula.append(criarIcone(opcao.icone));
    }
    if (opcao.cor) {
      pilula.append(criarElemento("span", { classe: "bolinha", "data-cor": opcao.cor }));
    }
    pilula.append(criarElemento("span", { texto: opcao.rotulo }));
    pilula.addEventListener("click", () => {
      escolher(valorEscolhido === opcao.valor ? null : opcao.valor);
      aoMudar(valorEscolhido);
    });
    pilulas.push({ pilula, valor: opcao.valor });
    elemento.append(pilula);
  }

  function escolher(novoValor) {
    valorEscolhido = novoValor;
    for (const { pilula, valor } of pilulas) {
      pilula.setAttribute("aria-pressed", valor === novoValor ? "true" : "false");
    }
  }

  escolher(valorInicial);
  return { elemento, obterValor: () => valorEscolhido, limpar: () => escolher(null) };
}
