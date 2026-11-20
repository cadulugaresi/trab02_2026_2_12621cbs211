import { criarElemento, gerarIdentificador } from "../elementos.js";
import { criarBotao, liberarBotao, marcarBotaoComoOcupado } from "./botoes.js";
import { abrirFlutuante } from "./flutuante.js";

let balaoAberto = null;

export function abrirBalaoDeExclusao({
  ancora,
  pergunta,
  explicacao,
  textoDoBotaoDeConfirmar = "Excluir",
  textoEnquantoConfirma = "Excluindo…",
  aoConfirmar,
}) {
  if (ancora.getAttribute("aria-expanded") === "true") {
    balaoAberto.fechar();
    return;
  }

  const identificadorDaPergunta = gerarIdentificador("pergunta");
  const identificadorDaExplicacao = gerarIdentificador("explicacao");
  const mensagemDeErro = criarElemento("p", {
    classe: "balao-de-exclusao-erro",
    role: "alert",
    hidden: true,
  });

  const botaoDeCancelar = criarBotao({ texto: "Cancelar", variacao: "secundario", pequeno: true });
  const botaoDeExcluir = criarBotao({
    texto: textoDoBotaoDeConfirmar,
    variacao: "perigo",
    pequeno: true,
  });

  const conteudo = criarElemento(
    "div",
    {
      classe: "balao-de-exclusao",
      role: "alertdialog",
      "aria-labelledby": identificadorDaPergunta,
      "aria-describedby": identificadorDaExplicacao,
    },
    [
      criarElemento("p", {
        classe: "balao-de-exclusao-pergunta",
        id: identificadorDaPergunta,
        texto: pergunta,
      }),
      criarElemento("p", {
        classe: "texto-de-apoio",
        id: identificadorDaExplicacao,
        texto: explicacao,
      }),
      mensagemDeErro,
      criarElemento("div", { classe: "balao-de-exclusao-botoes" }, [
        botaoDeCancelar,
        botaoDeExcluir,
      ]),
    ],
  );

  const balao = abrirFlutuante({
    conteudo: conteudo,
    ancora: ancora,
    preferencias: { lado: "abaixo", alinhamento: "fim" },
    aoFechar: () => {
      balaoAberto = null;
    },
  });
  balaoAberto = balao;

  botaoDeCancelar.addEventListener("click", () => balao.fechar());
  botaoDeExcluir.addEventListener("click", async () => {
    mensagemDeErro.hidden = true;
    marcarBotaoComoOcupado(botaoDeExcluir, textoEnquantoConfirma);
    try {
      await aoConfirmar();
      balao.fechar();
    } catch (erro) {
      liberarBotao(botaoDeExcluir);
      mensagemDeErro.textContent = erro.message;
      mensagemDeErro.hidden = false;
      balao.reposicionar();
    }
  });

  botaoDeCancelar.focus({ preventScroll: true });
}
