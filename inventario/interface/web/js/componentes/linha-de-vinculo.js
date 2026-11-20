import { criarElemento } from "../elementos.js";
import { formatarCvss } from "../formatos.js";
import { criarIcone } from "../icones.js";
import { NIVEIS_DE_GRAVIDADE } from "../rotulos.js";
import { abrirBalaoDeExclusao } from "./balao-de-exclusao.js";
import { criarBotao } from "./botoes.js";
import { criarPilulaDeStatusTrocavel } from "./pilula-de-status.js";

export function criarLinhaDeVinculo({
  nome,
  cvss,
  nivel,
  iconeDoAtivo,
  opcoesDeStatus,
  statusDeTratamento,
  enderecoDoNome,
  perguntaDoDesvinculo,
  aoMudarStatus,
  aoDesvincular,
  aoFalhar,
}) {
  const mostraUmAtivo = iconeDoAtivo !== undefined;
  const linha = criarElemento("li", {
    classe: mostraUmAtivo ? "linha-de-vinculo linha-de-vinculo-de-ativo" : "linha-de-vinculo",
  });
  const pilula = criarPilulaDeStatusTrocavel({
    rotulo: `Status de ${nome}`,
    opcoes: opcoesDeStatus,
    valor: statusDeTratamento,
    aoMudar: aoMudarStatus,
    aoFalhar: aoFalhar,
  });
  const botaoDeDesvincular = criarBotao({
    variacao: "icone",
    icone: "fechar",
    rotuloAcessivel: `Desvincular ${nome}`,
  });

  botaoDeDesvincular.addEventListener("click", () => {
    abrirBalaoDeExclusao({
      ancora: botaoDeDesvincular,
      pergunta: perguntaDoDesvinculo,
      explicacao: "O status de tratamento deste vínculo será perdido.",
      textoDoBotaoDeConfirmar: "Desvincular",
      textoEnquantoConfirma: "Desvinculando…",
      aoConfirmar: async () => {
        await aoDesvincular();
        linha.remove();
      },
    });
  });

  if (mostraUmAtivo) {
    linha.append(
      criarIcone(iconeDoAtivo, "linha-de-vinculo-icone"),
      criarNomeDoVinculo(nome, enderecoDoNome),
    );
  } else {
    linha.append(
      criarNivelDoVinculo(nivel),
      criarNomeDoVinculo(nome, enderecoDoNome),
      criarElemento("span", {
        classe: "linha-de-vinculo-cvss",
        texto: `CVSS ${formatarCvss(cvss)}`,
      }),
    );
  }
  linha.append(pilula.elemento, botaoDeDesvincular);
  return linha;
}

function criarNivelDoVinculo(nivel) {
  return criarElemento("span", { classe: "linha-de-vinculo-nivel" }, [
    criarElemento("span", { classe: "bolinha", "data-nivel": nivel }),
    criarElemento("span", {
      classe: "nome-do-nivel",
      "data-nivel": nivel,
      texto: NIVEIS_DE_GRAVIDADE[nivel].rotulo,
    }),
  ]);
}

function criarNomeDoVinculo(nome, enderecoDoNome) {
  if (enderecoDoNome) {
    return criarElemento("a", {
      classe: "linha-de-vinculo-nome",
      href: `#${enderecoDoNome}`,
      texto: nome,
    });
  }
  return criarElemento("span", { classe: "linha-de-vinculo-nome", texto: nome });
}
