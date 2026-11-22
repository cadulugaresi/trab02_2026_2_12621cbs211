import { criarBotao } from "../componentes/botoes.js";
import { criarFaixaDeErro } from "../componentes/faixa-de-erro.js";
import { abrirJanela } from "../componentes/janela.js";
import { criarElemento } from "../elementos.js";

const NAO_ENCONTRADO = 404;
const EXPLICACAO_QUANDO_NAO_EXISTE =
  "Este registro pode ter sido excluído, ou o endereço aponta para um ID que não existe.";

export function abrirJanelaCarregando(titulo, controles) {
  abrirJanela({
    titulo: titulo,
    corpo: criarElemento("div", { classe: "esqueleto-da-janela", "aria-hidden": "true" }, [
      criarElemento("span", { classe: "esqueleto esqueleto-numeros" }),
      criarElemento("span", { classe: "esqueleto esqueleto-texto" }),
      criarElemento("span", { classe: "esqueleto esqueleto-texto" }),
    ]),
    aoPedirFechamento: controles.pedirFechamento,
    aoVoltar: controles.voltar,
  });
}

export function abrirJanelaDeErro({
  erro,
  tituloQuandoNaoExiste,
  tituloQuandoFalha,
  aoTentarDeNovo,
  controles,
}) {
  if (erro.status === NAO_ENCONTRADO) {
    abrirJanela({
      titulo: tituloQuandoNaoExiste,
      corpo: criarElemento("p", { classe: "texto-de-apoio", texto: EXPLICACAO_QUANDO_NAO_EXISTE }),
      aoPedirFechamento: controles.pedirFechamento,
      aoVoltar: controles.voltar,
    });
    return;
  }
  const faixa = criarFaixaDeErro();
  abrirJanela({
    titulo: tituloQuandoFalha,
    corpo: criarElemento("div", { classe: "erro-da-janela" }, [
      faixa.elemento,
      criarBotao({ texto: "Tentar de novo", variacao: "secundario", aoClicar: aoTentarDeNovo }),
    ]),
    aoPedirFechamento: controles.pedirFechamento,
    aoVoltar: controles.voltar,
  });
  faixa.mostrar(erro.message);
}
