import { esconderComTransicao, mostrarComTransicao } from "../animacoes.js";
import { abrirCamada, devolverFoco, fecharCamada } from "../camadas.js";
import { criarElemento, gerarIdentificador } from "../elementos.js";
import { criarBotao } from "./botoes.js";

let janelaAberta = null;

export function abrirJanela({ titulo, subtitulo, acoes = [], corpo, aoPedirFechamento, aoVoltar }) {
  if (janelaAberta === null) {
    janelaAberta = criarJanelaVazia();
  }
  janelaAberta.aoPedirFechamento = aoPedirFechamento ?? fecharJanela;
  janelaAberta.fechamentoJaPedido = false;

  const { caixa, identificadorDoTitulo } = janelaAberta;
  caixa.replaceChildren(
    criarTopoDaJanela({ titulo, subtitulo, acoes, aoVoltar, identificadorDoTitulo }),
    criarElemento("div", { classe: "janela-corpo" }, [corpo]),
  );
  caixa.focus({ preventScroll: true });
}

export async function fecharJanela() {
  if (janelaAberta === null) {
    return;
  }
  const { camadaDaJanela, caixa, camada } = janelaAberta;
  janelaAberta = null;
  fecharCamada(camada);
  devolverFoco(camada);
  await esconderComTransicao(camadaDaJanela, caixa);
  camadaDaJanela.remove();
}

function pedirFechamento() {
  if (janelaAberta === null || janelaAberta.fechamentoJaPedido) {
    return;
  }
  janelaAberta.fechamentoJaPedido = true;
  janelaAberta.aoPedirFechamento();
}

function criarJanelaVazia() {
  const identificadorDoTitulo = gerarIdentificador("titulo-da-janela");
  const caixa = criarElemento("section", {
    classe: "janela",
    role: "dialog",
    "aria-modal": "true",
    "aria-labelledby": identificadorDoTitulo,
    tabindex: "-1",
  });
  const camadaDaJanela = criarElemento("div", { classe: "janela-camada" }, [
    criarElemento("div", { classe: "veu" }),
    caixa,
  ]);
  const camada = {
    areasDeDentro: [caixa],
    bloqueiaAPagina: true,
    pedirFechamento: pedirFechamento,
  };

  document.body.append(camadaDaJanela);
  abrirCamada(camada);
  mostrarComTransicao(camadaDaJanela);
  return { camadaDaJanela, caixa, camada, identificadorDoTitulo };
}

function criarTopoDaJanela({ titulo, subtitulo, acoes, aoVoltar, identificadorDoTitulo }) {
  const botaoDeVoltar = aoVoltar
    ? criarBotao({
        variacao: "icone",
        icone: "voltar",
        rotuloAcessivel: "Voltar",
        aoClicar: aoVoltar,
      })
    : null;
  if (botaoDeVoltar) {
    botaoDeVoltar.classList.add("janela-botao-voltar");
  }

  const titulos = criarElemento("div", { classe: "janela-titulos" }, [
    criarElemento("h2", { classe: "janela-titulo", id: identificadorDoTitulo, texto: titulo }),
    subtitulo ? criarElemento("p", { classe: "texto-de-apoio", texto: subtitulo }) : null,
  ]);
  const botaoDeFechar = criarBotao({
    variacao: "icone",
    icone: "fechar",
    rotuloAcessivel: "Fechar",
    aoClicar: pedirFechamento,
  });
  const areaDasAcoes = criarElemento("div", { classe: "janela-acoes" }, [...acoes, botaoDeFechar]);

  return criarElemento("header", { classe: "janela-topo" }, [botaoDeVoltar, titulos, areaDasAcoes]);
}
