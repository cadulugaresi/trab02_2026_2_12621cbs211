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
import { abrirJanelaCarregando, abrirJanelaDeErro } from "../janela-carregando.js";
import { criarSecaoDeDependencias } from "./dependencias-do-ativo.js";

export function abrirJanelaDoAtivo({ id }, controles) {
  abrirJanelaCarregando("Carregando ativo…", controles);

  carregarDadosDoAtivo(id)
    .then((dados) => {
      if (controles.continuaAberta()) {
        mostrarAtivo(dados, controles);
      }
    })
    .catch((erro) => {
      if (controles.continuaAberta()) {
        abrirJanelaDeErro({
          erro: erro,
          tituloQuandoNaoExiste: "Ativo não encontrado",
          tituloQuandoFalha: "Não foi possível abrir o ativo",
          aoTentarDeNovo: () => abrirJanelaDoAtivo({ id }, controles),
          controles: controles,
        });
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
  const textoQuandoVazia = criarElemento(
    "div",
    { classe: "secao-da-janela-vazia", hidden: vulnerabilidades.length > 0 },
    [
      criarElemento("p", {
        classe: "texto-de-apoio",
        texto: "Nenhuma vulnerabilidade vinculada a este ativo.",
      }),
      criarBotao({
        texto: "Vincular vulnerabilidade",
        variacao: "secundario",
        icone: "mais",
        pequeno: true,
        aoClicar: () => navegarPara(`/vinculos?ativo=${ativo.id}`),
      }),
    ],
  );

  for (const vulnerabilidade of vulnerabilidades) {
    lista.append(
      criarLinhaDeVinculo({
        nome: vulnerabilidade.nome_vulnerabilidade,
        cvss: vulnerabilidade.cvss,
        nivel: vulnerabilidade.nivel,
        enderecoDoNome: `/vulnerabilidades/${vulnerabilidade.id_vulnerabilidade}`,
        opcoesDeStatus: opcoes.statusDeTratamento,
        statusDeTratamento: vulnerabilidade.status_tratamento,
        perguntaDoDesvinculo: `Desvincular ${vulnerabilidade.nome_vulnerabilidade} de ${ativo.nome}?`,
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

