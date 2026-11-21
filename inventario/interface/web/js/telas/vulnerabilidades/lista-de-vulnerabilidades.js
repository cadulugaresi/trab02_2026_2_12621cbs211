import { listarVulnerabilidades } from "../../api.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarElemento } from "../../elementos.js";
import { formatarCvss } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { navegarPara } from "../../roteador.js";
import { NIVEIS_DE_GRAVIDADE } from "../../rotulos.js";
import {
  criarEstadoVazio,
  descreverQuantidade,
  mostrarEsqueletoNaLista,
} from "../estados-da-lista.js";

export function montarTelaDeVulnerabilidades(tela) {
  const faixa = criarFaixaDeErro();
  const contagem = criarElemento("p", {
    classe: "texto-de-apoio contagem-da-tela",
    "aria-live": "polite",
  });
  const lista = criarElemento("ul", {
    classe: "lista-de-vulnerabilidades",
    "aria-label": "Vulnerabilidades",
  });

  tela.append(
    criarElemento("header", { classe: "cabecalho-de-tela" }, [
      criarElemento("h1", { classe: "titulo-de-tela", texto: "Vulnerabilidades" }),
      contagem,
    ]),
    faixa.elemento,
    lista,
  );
  mostrarEsqueletoNaLista(lista);

  async function consultar() {
    try {
      const vulnerabilidades = await listarVulnerabilidades();
      faixa.esconder();
      mostrarVulnerabilidades(vulnerabilidades);
    } catch (erro) {
      faixa.mostrar(erro.message);
      lista.replaceChildren();
    }
  }

  function mostrarVulnerabilidades(vulnerabilidades) {
    contagem.textContent = descreverQuantidade(
      vulnerabilidades.length,
      "vulnerabilidade no catálogo",
      "vulnerabilidades no catálogo",
    );
    lista.replaceChildren();
    if (vulnerabilidades.length === 0) {
      lista.append(
        criarEstadoVazio({
          titulo: "Nenhuma vulnerabilidade cadastrada ainda",
          explicacao:
            "Cadastre as vulnerabilidades conhecidas com o CVSS de cada uma para depois vinculá-las aos ativos.",
          textoDoBotao: "Cadastrar a primeira vulnerabilidade",
          aoClicar: () => navegarPara("/vulnerabilidades/novo"),
        }),
      );
      return;
    }
    for (const vulnerabilidade of vulnerabilidades) {
      lista.append(criarLinhaDeVulnerabilidade(vulnerabilidade));
    }
  }

  consultar();
  return { atualizar: consultar };
}

function criarLinhaDeVulnerabilidade(vulnerabilidade) {
  const nivel = vulnerabilidade.nivel;
  const link = criarElemento(
    "a",
    {
      classe: "linha-de-vulnerabilidade",
      href: `#/vulnerabilidades/${vulnerabilidade.id_vulnerabilidade}`,
    },
    [
      criarElemento("span", { classe: "linha-de-vinculo-nivel" }, [
        criarElemento("span", { classe: "bolinha", "data-nivel": nivel }),
        criarElemento("span", {
          classe: "nome-do-nivel",
          "data-nivel": nivel,
          texto: NIVEIS_DE_GRAVIDADE[nivel].rotulo,
        }),
      ]),
      criarElemento("span", { classe: "linha-de-ativo-textos" }, [
        criarElemento("span", {
          classe: "linha-de-ativo-nome",
          texto: vulnerabilidade.nome_vulnerabilidade,
        }),
        criarElemento("span", {
          classe: "linha-de-ativo-detalhes",
          texto: `ID ${vulnerabilidade.id_vulnerabilidade}`,
        }),
      ]),
      criarElemento("span", {
        classe: "linha-de-vulnerabilidade-cvss",
        texto: `CVSS ${formatarCvss(vulnerabilidade.cvss)}`,
      }),
      criarIcone("setaParaDireita", "linha-de-ativo-seta"),
    ],
  );
  return criarElemento("li", {}, [link]);
}
