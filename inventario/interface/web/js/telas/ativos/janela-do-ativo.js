import {
  atualizarStatusDoVinculo,
  desvincularVulnerabilidade,
  excluirAtivo,
  listarAtivos,
  listarVulnerabilidadesDoAtivo,
} from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { abrirBalaoDeExclusao } from "../../componentes/balao-de-exclusao.js";
import { criarBotao } from "../../componentes/botoes.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { abrirJanela } from "../../componentes/janela.js";
import { criarLinhaDeVinculo } from "../../componentes/linha-de-vinculo.js";
import { criarNumerosDeRisco } from "../../componentes/numeros-de-risco.js";
import { criarPilulaDeStatus } from "../../componentes/pilula-de-status.js";
import { criarElemento } from "../../elementos.js";
import { formatarNumero } from "../../formatos.js";
import { carregarOpcoes, encontrarOpcao } from "../../opcoes.js";
import { buscarRiscosDoAtivo } from "../../riscos.js";
import { atualizarTelaAtual, navegarPara } from "../../roteador.js";
import {
  descreverAtivo,
  descreverCamposDoTipo,
  indexarAtivosPorId,
} from "./apresentacao-do-ativo.js";
import { criarSecaoDeDependencias } from "./dependencias-do-ativo.js";

export function abrirJanelaDoAtivo({ id }, controles) {
  abrirJanela({
    titulo: "Carregando ativo…",
    corpo: criarEsqueletoDaJanela(),
    aoPedirFechamento: controles.pedirFechamento,
    aoVoltar: controles.voltar,
  });

  carregarDadosDoAtivo(id)
    .then((dados) => {
      if (controles.continuaAberta()) {
        mostrarAtivo(dados, controles);
      }
    })
    .catch((erro) => {
      if (controles.continuaAberta()) {
        mostrarErroAoAbrir(erro, id, controles);
      }
    });
}

async function carregarDadosDoAtivo(idAtivo) {
  const [opcoes, ativos, vulnerabilidades] = await Promise.all([
    carregarOpcoes(),
    listarAtivos(),
    listarVulnerabilidadesDoAtivo(idAtivo),
  ]);
  const riscos = await buscarRiscosDoAtivo(idAtivo);
  const ativosPorId = indexarAtivosPorId(ativos);
  return { opcoes, ativosPorId, ativo: ativosPorId.get(idAtivo), vulnerabilidades, riscos };
}

function mostrarErroAoAbrir(erro, idAtivo, controles) {
  const ativoNaoExiste = erro.status === 404;
  const faixa = criarFaixaDeErro();
  const corpo = criarElemento("div", { classe: "erro-da-janela" }, [faixa.elemento]);
  if (!ativoNaoExiste) {
    corpo.append(
      criarBotao({
        texto: "Tentar de novo",
        variacao: "secundario",
        aoClicar: () => abrirJanelaDoAtivo({ id: idAtivo }, controles),
      }),
    );
  }
  abrirJanela({
    titulo: ativoNaoExiste ? "Ativo não encontrado" : "Não foi possível abrir o ativo",
    corpo: corpo,
    aoPedirFechamento: controles.pedirFechamento,
    aoVoltar: controles.voltar,
  });
  faixa.mostrar(erro.message);
}

function mostrarAtivo({ opcoes, ativosPorId, ativo, vulnerabilidades, riscos }, controles) {
  const faixa = criarFaixaDeErro();
  const numerosDeRisco = criarNumerosDeRisco(riscos.valores);
  if (riscos.valores === null) {
    numerosDeRisco.mostrarIndisponivel(riscos.mensagem);
  }

  function mostrarFalha(erro) {
    faixa.mostrar(erro.message);
  }

  async function atualizarRiscos() {
    try {
      const novosRiscos = await buscarRiscosDoAtivo(ativo.id);
      if (novosRiscos.valores === null) {
        numerosDeRisco.mostrarIndisponivel(novosRiscos.mensagem);
      } else {
        numerosDeRisco.animarAte(novosRiscos.valores);
      }
    } catch (erro) {
      mostrarFalha(erro);
    }
  }

  const corpo = criarElemento("div", {}, [
    faixa.elemento,
    criarFichaDoAtivo(ativo, opcoes),
    numerosDeRisco.elemento,
    criarSecaoDeVulnerabilidades({ ativo, vulnerabilidades, opcoes, atualizarRiscos, mostrarFalha }),
    criarSecaoDeDependencias({
      idAtivo: ativo.id,
      ativosPorId: ativosPorId,
      aoMudar: () => {
        atualizarRiscos();
        atualizarTelaAtual();
      },
      mostrarFalha: mostrarFalha,
    }),
  ]);

  abrirJanela({
    titulo: ativo.nome,
    subtitulo: descreverAtivo(ativo, opcoes),
    acoes: criarAcoesDoAtivo(ativo, controles),
    corpo: corpo,
    aoPedirFechamento: controles.pedirFechamento,
    aoVoltar: controles.voltar,
  });
}

function criarFichaDoAtivo(ativo, opcoes) {
  const status = encontrarOpcao(opcoes.statusDoAtivo, ativo.status);
  const ficha = criarElemento("div", { classe: "ficha-do-ativo" });
  if (status) {
    ficha.append(criarPilulaDeStatus({ rotulo: status.rotulo, cor: status.cor }));
  }
  ficha.append(
    criarElemento("span", {
      texto: `Fator de exposição ${formatarNumero(ativo.fator_exposicao)}`,
    }),
  );
  for (const campo of descreverCamposDoTipo(ativo, opcoes)) {
    ficha.append(criarElemento("span", { texto: campo }));
  }
  return ficha;
}

function criarSecaoDeVulnerabilidades({
  ativo,
  vulnerabilidades,
  opcoes,
  atualizarRiscos,
  mostrarFalha,
}) {
  const lista = criarElemento("ul", { classe: "lista-de-vinculos" });
  const textoQuandoVazia = criarElemento("p", {
    classe: "texto-de-apoio secao-da-janela-vazia",
    texto: "Nenhuma vulnerabilidade vinculada a este ativo.",
    hidden: vulnerabilidades.length > 0,
  });

  for (const vulnerabilidade of vulnerabilidades) {
    lista.append(
      criarLinhaDeVinculo({
        nome: vulnerabilidade.nome_vulnerabilidade,
        cvss: vulnerabilidade.cvss,
        nivel: vulnerabilidade.nivel,
        opcoesDeStatus: opcoes.statusDeTratamento,
        statusDeTratamento: vulnerabilidade.status_tratamento,
        aoMudarStatus: async (novoStatus) => {
          await atualizarStatusDoVinculo(ativo.id, vulnerabilidade.id_vulnerabilidade, novoStatus);
          atualizarRiscos();
        },
        aoDesvincular: async () => {
          await desvincularVulnerabilidade(ativo.id, vulnerabilidade.id_vulnerabilidade);
          textoQuandoVazia.hidden = lista.children.length > 1;
          mostrarAvisoDeSucesso("Vulnerabilidade desvinculada");
          atualizarRiscos();
          atualizarTelaAtual();
        },
        aoFalhar: mostrarFalha,
      }),
    );
  }

  return criarElemento("section", { classe: "secao-da-janela" }, [
    criarElemento("h3", {
      classe: "titulo-de-secao secao-da-janela-titulo",
      texto: "Vulnerabilidades vinculadas",
    }),
    lista,
    textoQuandoVazia,
  ]);
}

function criarAcoesDoAtivo(ativo, controles) {
  const botaoDeEditar = criarBotao({
    texto: "Editar",
    variacao: "secundario",
    icone: "editar",
    pequeno: true,
    aoClicar: () => navegarPara(`/ativos/${ativo.id}/editar`),
  });
  const botaoDeExcluir = criarBotao({
    texto: "Excluir",
    variacao: "secundario",
    icone: "excluir",
    pequeno: true,
  });
  botaoDeExcluir.addEventListener("click", () => {
    abrirBalaoDeExclusao({
      ancora: botaoDeExcluir,
      pergunta: `Excluir ${ativo.nome}?`,
      explicacao: "Os vínculos e as dependências dele também serão removidos.",
      aoConfirmar: async () => {
        await excluirAtivo(ativo.id);
        controles.pedirFechamento();
        atualizarTelaAtual();
        mostrarAvisoDeSucesso("Ativo excluído");
      },
    });
  });
  return [botaoDeEditar, botaoDeExcluir];
}

function criarEsqueletoDaJanela() {
  return criarElemento("div", { classe: "esqueleto-da-janela", "aria-hidden": "true" }, [
    criarElemento("span", { classe: "esqueleto esqueleto-numeros" }),
    criarElemento("span", { classe: "esqueleto esqueleto-texto" }),
    criarElemento("span", { classe: "esqueleto esqueleto-texto" }),
  ]);
}
