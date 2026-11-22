import { criarElemento, gerarIdentificador } from "../elementos.js";
import { criarIcone } from "../icones.js";

export function criarSegmentado({ rotulo, opcoes, valor, variacao = "padrao", aoMudar }) {
  const nomeDoGrupo = gerarIdentificador("segmentado");
  const elemento = criarElemento("div", {
    classe: `segmentado segmentado-${variacao}`,
    role: "radiogroup",
    "aria-label": rotulo,
  });
  elemento.style.setProperty("--quantidade-de-opcoes", String(opcoes.length));
  const cartao = criarElemento("span", { classe: "segmentado-cartao", "aria-hidden": "true" });
  const camadaEscolhida = criarElemento("div", {
    classe: "segmentado-camada-escolhida",
    "aria-hidden": "true",
  });
  const entradas = [];

  for (const [indice, opcao] of opcoes.entries()) {
    const entrada = criarElemento("input", {
      type: "radio",
      classe: "segmentado-entrada",
      name: nomeDoGrupo,
      value: String(opcao.valor),
    });
    entrada.addEventListener("change", () => {
      moverCartaoPara(indice);
      if (aoMudar) {
        aoMudar(opcao.valor);
      }
    });
    entradas.push(entrada);
    elemento.append(
      criarElemento("label", { classe: "segmentado-opcao" }, [entrada, ...criarConteudo(opcao)]),
    );
    camadaEscolhida.append(criarElemento("span", {}, criarConteudo(opcao)));
  }
  elemento.prepend(cartao);
  elemento.append(camadaEscolhida);

  function moverCartaoPara(indice) {
    const larguraDeUmaOpcao = 100 / opcoes.length;
    const recorteDaEsquerda = indice * larguraDeUmaOpcao;
    const recorteDaDireita = 100 - (indice + 1) * larguraDeUmaOpcao;
    cartao.style.transform = `translateX(${indice * 100}%)`;
    camadaEscolhida.style.clipPath =
      `inset(0 ${recorteDaDireita}% 0 ${recorteDaEsquerda}% round var(--raio-do-cartao))`;
  }

  function definirValor(novoValor) {
    for (const [indice, opcao] of opcoes.entries()) {
      if (opcao.valor === novoValor) {
        entradas[indice].checked = true;
        moverCartaoPara(indice);
      }
    }
  }

  definirValor(valor);
  return { elemento, definirValor };
}

function criarConteudo(opcao) {
  const conteudo = [];
  if (opcao.icone) {
    conteudo.push(criarIcone(opcao.icone));
  }
  conteudo.push(criarElemento("span", { texto: opcao.rotulo }));
  return conteudo;
}
