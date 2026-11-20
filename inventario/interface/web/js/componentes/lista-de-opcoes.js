import { criarElemento, gerarIdentificador } from "../elementos.js";
import { criarIcone } from "../icones.js";
import { abrirFlutuante } from "./flutuante.js";

export function abrirListaDeOpcoes({ ancora, rotulo, opcoes, valorEscolhido, aoEscolher }) {
  const lista = criarElemento("ul", {
    classe: "lista-de-opcoes",
    role: "listbox",
    tabindex: "-1",
    "aria-label": rotulo,
  });
  const itens = [];
  let indiceAtivo = 0;

  for (const opcao of opcoes) {
    const estaEscolhida = opcao.valor === valorEscolhido;
    const item = criarItemDeOpcao(opcao, estaEscolhida);
    const indiceDoItem = itens.length;
    if (estaEscolhida) {
      indiceAtivo = indiceDoItem;
    }
    item.addEventListener("click", () => escolher(opcao));
    item.addEventListener("pointermove", () => {
      indiceAtivo = indiceDoItem;
      marcarItemAtivo(itens, lista, indiceAtivo, false);
    });
    itens.push(item);
    lista.append(item);
  }

  const flutuante = abrirFlutuante({
    conteudo: lista,
    ancora: ancora,
    preferencias: { mesmaLarguraDaAncora: true },
  });

  function escolher(opcao) {
    flutuante.fechar();
    aoEscolher(opcao);
  }

  lista.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter" || evento.key === " ") {
      evento.preventDefault();
      escolher(opcoes[indiceAtivo]);
      return;
    }
    const proximoIndice = calcularIndicePeloTeclado(evento, indiceAtivo, itens.length);
    if (proximoIndice !== null) {
      evento.preventDefault();
      indiceAtivo = proximoIndice;
      marcarItemAtivo(itens, lista, indiceAtivo);
    }
  });

  marcarItemAtivo(itens, lista, indiceAtivo);
  lista.focus({ preventScroll: true });
  return flutuante;
}

export function criarItemDeOpcao(opcao, estaEscolhida) {
  const item = criarElemento("li", {
    classe: "opcao",
    role: "option",
    id: gerarIdentificador("opcao"),
    "aria-selected": estaEscolhida ? "true" : "false",
  });
  if (opcao.cor) {
    item.append(criarElemento("span", { classe: "bolinha", "data-cor": opcao.cor }));
  }
  if (opcao.icone) {
    item.append(criarIcone(opcao.icone));
  }
  item.append(criarElemento("span", { classe: "opcao-texto", texto: opcao.rotulo }));
  if (opcao.detalhe) {
    item.append(criarElemento("span", { classe: "opcao-detalhe", texto: opcao.detalhe }));
  }
  if (estaEscolhida) {
    item.append(criarIcone("confirmado", "opcao-marca"));
  }
  return item;
}

export function marcarItemAtivo(itens, elementoComFoco, indiceAtivo, rolarAteOItem = true) {
  for (const [indice, item] of itens.entries()) {
    item.toggleAttribute("data-ativa", indice === indiceAtivo);
  }
  const itemAtivo = itens[indiceAtivo];
  if (itemAtivo === undefined) {
    elementoComFoco.removeAttribute("aria-activedescendant");
    return;
  }
  elementoComFoco.setAttribute("aria-activedescendant", itemAtivo.id);
  if (rolarAteOItem) {
    itemAtivo.scrollIntoView({ block: "nearest" });
  }
}

export function calcularIndicePeloTeclado(evento, indiceAtual, quantidadeDeItens) {
  if (quantidadeDeItens === 0) {
    return null;
  }
  if (evento.key === "ArrowDown") {
    return Math.min(indiceAtual + 1, quantidadeDeItens - 1);
  }
  if (evento.key === "ArrowUp") {
    return Math.max(indiceAtual - 1, 0);
  }
  if (evento.key === "Home") {
    return 0;
  }
  if (evento.key === "End") {
    return quantidadeDeItens - 1;
  }
  return null;
}
