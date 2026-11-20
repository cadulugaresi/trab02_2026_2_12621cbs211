import { criarBotao } from "../componentes/botoes.js";
import { criarFaixaDeErro } from "../componentes/faixa-de-erro.js";
import { abrirJanela } from "../componentes/janela.js";
import { criarElemento } from "../elementos.js";

const NAO_ENCONTRADO = 404;

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

export function abrirJanelaDeErro({ erro, tituloQuandoNaoExiste, tituloQuandoFalha, aoTentarDeNovo, controles }) {
  const naoExiste = erro.status === NAO_ENCONTRADO;
  const faixa = criarFaixaDeErro();
  const corpo = criarElemento("div", { classe: "erro-da-janela" }, [faixa.elemento]);
  if (!naoExiste) {
    corpo.append(
      criarBotao({ texto: "Tentar de novo", variacao: "secundario", aoClicar: aoTentarDeNovo }),
    );
  }
  abrirJanela({
    titulo: naoExiste ? tituloQuandoNaoExiste : tituloQuandoFalha,
    corpo: corpo,
    aoPedirFechamento: controles.pedirFechamento,
    aoVoltar: controles.voltar,
  });
  faixa.mostrar(erro.message);
}
