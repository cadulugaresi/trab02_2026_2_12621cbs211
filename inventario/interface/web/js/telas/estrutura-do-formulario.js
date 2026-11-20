import { criarBotao } from "../componentes/botoes.js";
import { criarFaixaDeErro } from "../componentes/faixa-de-erro.js";
import { criarElemento } from "../elementos.js";
import { voltarOuIrPara } from "../roteador.js";

export function criarEstruturaDoFormulario({ titulo, textoDoBotao, enderecoDeVolta }) {
  const faixa = criarFaixaDeErro();
  const subtitulo = criarElemento("p", { classe: "texto-de-apoio" });
  const areaDosCampos = criarElemento("div", { classe: "campos-do-formulario" });
  const botaoDeSalvar = criarBotao({ texto: textoDoBotao });
  botaoDeSalvar.type = "submit";
  botaoDeSalvar.disabled = true;

  const formulario = criarElemento("form", { classe: "formulario-de-ajustes", novalidate: true }, [
    criarElemento("header", { classe: "cabecalho-do-formulario" }, [
      criarElemento("div", { classe: "cabecalho-de-tela-textos" }, [
        criarElemento("h1", { classe: "titulo-de-tela", texto: titulo }),
        subtitulo,
      ]),
      criarElemento("div", { classe: "cabecalho-do-formulario-botoes" }, [
        criarBotao({
          texto: "Cancelar",
          variacao: "secundario",
          aoClicar: () => voltarOuIrPara(enderecoDeVolta),
        }),
        botaoDeSalvar,
      ]),
    ]),
    faixa.elemento,
    areaDosCampos,
  ]);

  return { formulario, subtitulo, areaDosCampos, faixa, botaoDeSalvar };
}

export function criarGrupoDoFormulario(titulo, filhos) {
  return criarElemento("section", { classe: "grupo-de-ajustes" }, [
    criarElemento("h2", { classe: "titulo-de-secao", texto: titulo }),
    ...filhos,
  ]);
}

export function mostrarErrosNasLinhas(erros, linhas) {
  for (const erro of erros) {
    linhas[erro.campo].mostrarErro(erro.mensagem);
  }
  linhas[erros[0].campo].alvo.focus();
}
