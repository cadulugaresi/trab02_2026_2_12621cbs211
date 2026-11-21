import { criarElemento } from "../../elementos.js";

const MENOR_ALTURA_DA_BARRA = 2;

export function criarBarrasDosSetores(setores) {
  let maiorQuantidade = 0;
  for (const setor of setores) {
    maiorQuantidade = Math.max(maiorQuantidade, setor.quantidade);
  }

  const itens = [];
  for (const setor of setores) {
    const proporcao = maiorQuantidade > 0 ? (setor.quantidade / maiorQuantidade) * 100 : 0;
    itens.push(
      criarElemento("li", { classe: "barra-do-setor", "data-destaque": setor.destaque }, [
        criarElemento("span", { classe: "barra-do-setor-numero", texto: String(setor.quantidade) }),
        criarElemento("span", { classe: "barra-do-setor-trilho", "aria-hidden": "true" }, [
          criarElemento("span", {
            classe: "barra-do-setor-coluna",
            style: `height: max(${MENOR_ALTURA_DA_BARRA}px, ${proporcao}%)`,
          }),
        ]),
        criarElemento("span", { classe: "barra-do-setor-nome", texto: setor.opcao.rotulo }),
      ]),
    );
  }
  return criarElemento("ol", { classe: "barras-dos-setores" }, itens);
}
