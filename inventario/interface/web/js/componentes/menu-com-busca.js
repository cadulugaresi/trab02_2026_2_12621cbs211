import { criarElemento, gerarIdentificador } from "../elementos.js";
import { normalizarParaBusca } from "../formatos.js";
import { criarIcone } from "../icones.js";
import { abrirFlutuante } from "./flutuante.js";
import { encontrarOpcao } from "../opcoes.js";
import { calcularIndicePeloTeclado, criarItemDeOpcao, marcarItemAtivo } from "./lista-de-opcoes.js";

export function criarMenuComBusca({
  rotulo,
  itens = [],
  valor = null,
  textoQuandoVazio,
  textoSemResultado,
  aoMudar,
}) {
  let itensAtuais = itens;
  let valorAtual = valor;
  let menuAberto = null;

  const texto = criarElemento("span", { classe: "campo-gatilho-texto" });
  const detalhe = criarElemento("span", { classe: "campo-gatilho-detalhe" });
  const gatilho = criarElemento(
    "button",
    {
      type: "button",
      classe: "campo campo-gatilho",
      id: gerarIdentificador("menu-com-busca"),
      "aria-haspopup": "listbox",
      "aria-expanded": "false",
    },
    [texto, detalhe, criarIcone("setaParaBaixo", "seta")],
  );

  function definirValor(novoValor) {
    valorAtual = novoValor;
    const itemEscolhido = encontrarOpcao(itensAtuais, novoValor);
    texto.textContent = itemEscolhido ? itemEscolhido.rotulo : textoQuandoVazio;
    detalhe.textContent = itemEscolhido ? `ID ${itemEscolhido.valor}` : "";
    gatilho.toggleAttribute("data-vazio", itemEscolhido === undefined);
    gatilho.setAttribute("aria-label", `${rotulo}: ${texto.textContent} ${detalhe.textContent}`);
  }

  function definirItens(novosItens) {
    itensAtuais = novosItens;
    definirValor(valorAtual);
  }

  function escolher(item) {
    menuAberto.fechar();
    definirValor(item.valor);
    gatilho.dispatchEvent(new Event("change", { bubbles: true }));
    if (aoMudar) {
      aoMudar(item.valor, item);
    }
  }

  function abrir() {
    menuAberto = abrirMenuDeBusca({
      ancora: gatilho,
      rotulo: rotulo,
      itens: itensAtuais,
      valorEscolhido: valorAtual,
      textoSemResultado: textoSemResultado,
      aoEscolher: escolher,
    });
  }

  gatilho.addEventListener("click", () => {
    if (gatilho.getAttribute("aria-expanded") === "true") {
      menuAberto.fechar();
      return;
    }
    abrir();
  });

  gatilho.addEventListener("keydown", (evento) => {
    if (evento.key === "ArrowDown" || evento.key === "ArrowUp") {
      evento.preventDefault();
      abrir();
    }
  });

  definirValor(valorAtual);
  return { elemento: gatilho, obterValor: () => valorAtual, definirValor, definirItens };
}

function abrirMenuDeBusca({ ancora, rotulo, itens, valorEscolhido, textoSemResultado, aoEscolher }) {
  const identificadorDaLista = gerarIdentificador("lista");
  const lista = criarElemento("ul", {
    classe: "lista-de-opcoes",
    role: "listbox",
    id: identificadorDaLista,
    "aria-label": rotulo,
  });
  const busca = criarElemento("input", {
    type: "text",
    classe: "busca-do-menu-entrada",
    role: "combobox",
    "aria-expanded": "true",
    "aria-controls": identificadorDaLista,
    "aria-autocomplete": "list",
    "aria-label": `Buscar ${rotulo.toLowerCase()} por nome ou ID`,
    placeholder: "Buscar por nome ou ID",
    autocomplete: "off",
    spellcheck: "false",
  });
  const caixaDaBusca = criarElemento("div", { classe: "busca-do-menu" }, [
    criarIcone("buscar"),
    busca,
  ]);

  let itensVisiveis = [];
  let elementosVisiveis = [];
  let indiceAtivo = 0;

  function mostrarItens() {
    itensVisiveis = filtrarItens(itens, busca.value);
    elementosVisiveis = [];
    lista.replaceChildren();
    for (const item of itensVisiveis) {
      const indiceDoItem = elementosVisiveis.length;
      const elemento = criarItemDeOpcao(
        { ...item, detalhe: `ID ${item.valor}` },
        item.valor === valorEscolhido,
      );
      elemento.addEventListener("click", () => aoEscolher(item));
      elemento.addEventListener("pointermove", () => {
        indiceAtivo = indiceDoItem;
        marcarItemAtivo(elementosVisiveis, busca, indiceAtivo, false);
      });
      elementosVisiveis.push(elemento);
      lista.append(elemento);
    }
    if (itensVisiveis.length === 0) {
      lista.append(criarElemento("li", { classe: "opcao-vazia", texto: textoSemResultado }));
    }
    indiceAtivo = 0;
    marcarItemAtivo(elementosVisiveis, busca, indiceAtivo);
  }

  busca.addEventListener("input", mostrarItens);
  busca.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter") {
      evento.preventDefault();
      if (itensVisiveis.length > 0) {
        aoEscolher(itensVisiveis[indiceAtivo]);
      }
      return;
    }
    const proximoIndice = calcularIndicePeloTeclado(evento, indiceAtivo, itensVisiveis.length);
    if (proximoIndice !== null) {
      evento.preventDefault();
      indiceAtivo = proximoIndice;
      marcarItemAtivo(elementosVisiveis, busca, indiceAtivo);
    }
  });

  const conteudo = criarElemento("div", { classe: "menu-com-busca" }, [caixaDaBusca, lista]);
  mostrarItens();
  const flutuante = abrirFlutuante({
    conteudo: conteudo,
    ancora: ancora,
    preferencias: { mesmaLarguraDaAncora: true },
  });
  busca.focus({ preventScroll: true });
  return flutuante;
}

function filtrarItens(itens, textoDaBusca) {
  const busca = normalizarParaBusca(textoDaBusca);
  const itensEncontrados = [];
  for (const item of itens) {
    const nomeCombina = normalizarParaBusca(item.rotulo).includes(busca);
    const idCombina = String(item.valor).startsWith(busca);
    if (busca === "" || nomeCombina || idCombina) {
      itensEncontrados.push(item);
    }
  }
  return itensEncontrados;
}
