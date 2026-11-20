import { criarElemento } from "../elementos.js";
import { criarIcone } from "../icones.js";
import { abrirListaDeOpcoes } from "./lista-de-opcoes.js";
import { encontrarOpcao } from "./menu-suspenso.js";

export function criarPilulaDeStatus({ rotulo, cor }) {
  return criarElemento("span", { classe: "pilula-de-status" }, [
    criarElemento("span", { classe: "bolinha", "data-cor": cor }),
    criarElemento("span", { texto: rotulo }),
  ]);
}

export function criarPilulaDeStatusTrocavel({ rotulo, opcoes, valor, aoMudar, aoFalhar }) {
  let valorAtual = valor;
  let listaAberta = null;

  const bolinha = criarElemento("span", { classe: "bolinha" });
  const texto = criarElemento("span");
  const pilula = criarElemento(
    "button",
    {
      type: "button",
      classe: "pilula-de-status",
      "aria-haspopup": "listbox",
      "aria-expanded": "false",
    },
    [bolinha, texto, criarIcone("setaParaBaixo", "seta")],
  );

  function mostrarValor(novoValor) {
    valorAtual = novoValor;
    const opcao = encontrarOpcao(opcoes, novoValor);
    texto.textContent = opcao ? opcao.rotulo : "";
    bolinha.setAttribute("data-cor", opcao ? opcao.cor : "cinza");
    pilula.setAttribute("aria-label", `${rotulo}: ${texto.textContent}. Trocar status`);
  }

  async function trocarPara(opcao) {
    const valorAnterior = valorAtual;
    if (opcao.valor === valorAnterior) {
      return;
    }
    mostrarValor(opcao.valor);
    try {
      if (aoMudar) {
        await aoMudar(opcao.valor);
      }
    } catch (erro) {
      mostrarValor(valorAnterior);
      if (aoFalhar) {
        aoFalhar(erro);
      }
    }
  }

  pilula.addEventListener("click", () => {
    if (pilula.getAttribute("aria-expanded") === "true") {
      listaAberta.fechar();
      return;
    }
    listaAberta = abrirListaDeOpcoes({
      ancora: pilula,
      rotulo: rotulo,
      opcoes: opcoes,
      valorEscolhido: valorAtual,
      aoEscolher: trocarPara,
    });
  });

  mostrarValor(valorAtual);
  return { elemento: pilula, obterValor: () => valorAtual, definirValor: mostrarValor };
}
