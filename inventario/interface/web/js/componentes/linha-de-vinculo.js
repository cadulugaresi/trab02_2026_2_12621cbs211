import { criarElemento } from "../elementos.js";
import { formatarCvss } from "../formatos.js";
import { NIVEIS_DE_GRAVIDADE } from "../rotulos.js";
import { criarBotao } from "./botoes.js";
import { criarPilulaDeStatusTrocavel } from "./pilula-de-status.js";

export function criarLinhaDeVinculo({
  nome,
  cvss,
  nivel,
  opcoesDeStatus,
  statusDeTratamento,
  enderecoDoNome,
  aoMudarStatus,
  aoDesvincular,
  aoFalhar,
}) {
  const linha = criarElemento("li", { classe: "linha-de-vinculo" });
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

  botaoDeDesvincular.addEventListener("click", async () => {
    botaoDeDesvincular.disabled = true;
    try {
      await aoDesvincular();
      linha.remove();
    } catch (erro) {
      botaoDeDesvincular.disabled = false;
      aoFalhar(erro);
    }
  });

  linha.append(
    criarElemento("span", { classe: "linha-de-vinculo-nivel" }, [
      criarElemento("span", { classe: "bolinha", "data-nivel": nivel }),
      criarElemento("span", {
        classe: "nome-do-nivel",
        "data-nivel": nivel,
        texto: NIVEIS_DE_GRAVIDADE[nivel].rotulo,
      }),
    ]),
    criarNomeDoVinculo(nome, enderecoDoNome),
    criarElemento("span", { classe: "linha-de-vinculo-cvss", texto: `CVSS ${formatarCvss(cvss)}` }),
    pilula.elemento,
    botaoDeDesvincular,
  );
  return linha;
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
