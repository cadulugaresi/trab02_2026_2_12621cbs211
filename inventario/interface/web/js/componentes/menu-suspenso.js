import { criarElemento, gerarIdentificador } from "../elementos.js";
import { criarIcone } from "../icones.js";
import { encontrarOpcao } from "../opcoes.js";
import { abrirListaDeOpcoes } from "./lista-de-opcoes.js";

export function criarMenuSuspenso({ rotulo, opcoes = [], valor = null, textoQuandoVazio, aoMudar }) {
  let opcoesAtuais = opcoes;
  let valorAtual = valor;
  let listaAberta = null;

  const bolinha = criarElemento("span", { classe: "bolinha", hidden: true });
  const texto = criarElemento("span", { classe: "campo-gatilho-texto" });
  const gatilho = criarElemento(
    "button",
    {
      type: "button",
      classe: "campo campo-gatilho",
      id: gerarIdentificador("menu"),
      "aria-haspopup": "listbox",
      "aria-expanded": "false",
    },
    [bolinha, texto, criarIcone("setaParaBaixo", "seta")],
  );

  function definirValor(novoValor) {
    valorAtual = novoValor;
    const opcaoEscolhida = encontrarOpcao(opcoesAtuais, novoValor);
    const textoExibido = opcaoEscolhida ? opcaoEscolhida.rotulo : textoQuandoVazio;
    texto.textContent = textoExibido;
    gatilho.toggleAttribute("data-vazio", opcaoEscolhida === undefined);
    gatilho.setAttribute("aria-label", `${rotulo}: ${textoExibido}`);
    bolinha.hidden = !(opcaoEscolhida && opcaoEscolhida.cor);
    if (opcaoEscolhida && opcaoEscolhida.cor) {
      bolinha.setAttribute("data-cor", opcaoEscolhida.cor);
    }
  }

  function definirOpcoes(novasOpcoes) {
    opcoesAtuais = novasOpcoes;
    definirValor(valorAtual);
  }

  function abrir() {
    if (opcoesAtuais.length === 0) {
      return;
    }
    listaAberta = abrirListaDeOpcoes({
      ancora: gatilho,
      rotulo: rotulo,
      opcoes: opcoesAtuais,
      valorEscolhido: valorAtual,
      aoEscolher: (opcao) => {
        definirValor(opcao.valor);
        gatilho.dispatchEvent(new Event("change", { bubbles: true }));
        if (aoMudar) {
          aoMudar(opcao.valor, opcao);
        }
      },
    });
  }

  gatilho.addEventListener("click", () => {
    if (gatilho.getAttribute("aria-expanded") === "true") {
      listaAberta.fechar();
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
  return { elemento: gatilho, obterValor: () => valorAtual, definirValor, definirOpcoes };
}
