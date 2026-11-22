import { criarBotao } from "../componentes/botoes.js";
import { criarElemento } from "../elementos.js";

const LINHAS_DO_ESQUELETO = 4;

export function mostrarEsqueletoNaLista(lista) {
  lista.replaceChildren();
  for (let posicao = 0; posicao < LINHAS_DO_ESQUELETO; posicao += 1) {
    lista.append(
      criarElemento("li", { classe: "linha-esqueleto", "aria-hidden": "true" }, [
        criarElemento("span", { classe: "esqueleto esqueleto-icone" }),
        criarElemento("span", { classe: "esqueleto esqueleto-texto" }),
      ]),
    );
  }
}

export function criarEstadoVazio({ titulo, explicacao, textoDoBotao, aoClicar, variacao }) {
  return criarElemento("li", { classe: "estado-vazio" }, [
    criarElemento("p", { classe: "estado-vazio-titulo", texto: titulo }),
    criarElemento("p", { classe: "texto-de-apoio", texto: explicacao }),
    criarBotao({ texto: textoDoBotao, variacao: variacao ?? "principal", aoClicar: aoClicar }),
  ]);
}

export function descreverQuantidade(quantidade, singular, plural) {
  return `${quantidade} ${quantidade === 1 ? singular : plural}`;
}
