import { buscarVulnerabilidade, excluirVulnerabilidade, listarAtivos } from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { abrirBalaoDeExclusao } from "../../componentes/balao-de-exclusao.js";
import { criarBotao } from "../../componentes/botoes.js";
import { abrirJanela } from "../../componentes/janela.js";
import { criarPilulaDeStatus } from "../../componentes/pilula-de-status.js";
import { criarElemento } from "../../elementos.js";
import { formatarCvss } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { carregarOpcoes, encontrarOpcao, encontrarValorPeloNome } from "../../opcoes.js";
import { atualizarTelaAtual, navegarPara } from "../../roteador.js";
import { NIVEIS_DE_GRAVIDADE } from "../../rotulos.js";
import { iconeDoTipo } from "../ativos/apresentacao-do-ativo.js";
import { abrirJanelaCarregando, abrirJanelaDeErro } from "../janela-carregando.js";

export function abrirJanelaDaVulnerabilidade({ id }, controles) {
  abrirJanelaCarregando("Carregando vulnerabilidade…", controles);

  carregarDadosDaVulnerabilidade(id)
    .then((dados) => {
      if (controles.continuaAberta()) {
        mostrarVulnerabilidade(dados, controles);
      }
    })
    .catch((erro) => {
      if (controles.continuaAberta()) {
        abrirJanelaDeErro({
          erro: erro,
          tituloQuandoNaoExiste: "Vulnerabilidade não encontrada",
          tituloQuandoFalha: "Não foi possível abrir a vulnerabilidade",
          aoTentarDeNovo: () => abrirJanelaDaVulnerabilidade({ id }, controles),
          controles: controles,
        });
      }
    });
}

async function carregarDadosDaVulnerabilidade(idVulnerabilidade) {
  const [opcoes, vulnerabilidade, ativos] = await Promise.all([
    carregarOpcoes(),
    buscarVulnerabilidade(idVulnerabilidade),
    listarAtivos(),
  ]);
  return { opcoes, vulnerabilidade, ativos };
}

function mostrarVulnerabilidade({ opcoes, vulnerabilidade, ativos }, controles) {
  const valorDeCorrigida = encontrarValorPeloNome(opcoes.statusDeTratamento, "CORRIGIDA");
  const { afetadosAgora, jaCorrigidos } = separarAtivosPeloStatus(
    ativos,
    vulnerabilidade.id_vulnerabilidade,
    valorDeCorrigida,
  );

  const corpo = criarElemento("div", {}, [
    criarDestaqueDoCvss(vulnerabilidade),
    criarSecaoDeAtivos({
      titulo: "Afetados agora",
      vinculos: afetadosAgora,
      opcoes: opcoes,
      textoQuandoVazia: "Nenhum ativo está afetado por esta vulnerabilidade agora.",
      apagada: false,
    }),
    jaCorrigidos.length > 0
      ? criarSecaoDeAtivos({
          titulo: "Já corrigida em",
          vinculos: jaCorrigidos,
          opcoes: opcoes,
          textoQuandoVazia: "",
          apagada: true,
        })
      : null,
  ]);

  abrirJanela({
    titulo: vulnerabilidade.nome_vulnerabilidade,
    subtitulo: `ID ${vulnerabilidade.id_vulnerabilidade}`,
    acoes: criarAcoesDaVulnerabilidade(vulnerabilidade, controles),
    corpo: corpo,
    aoPedirFechamento: controles.pedirFechamento,
    aoVoltar: controles.voltar,
  });
}

function separarAtivosPeloStatus(ativos, idVulnerabilidade, valorDeCorrigida) {
  const afetadosAgora = [];
  const jaCorrigidos = [];
  for (const ativo of ativos) {
    for (const vinculo of ativo.vulnerabilidades) {
      if (vinculo.id_vulnerabilidade !== idVulnerabilidade) {
        continue;
      }
      const ativoComStatus = { ativo, statusDeTratamento: vinculo.status_tratamento };
      if (vinculo.status_tratamento === valorDeCorrigida) {
        jaCorrigidos.push(ativoComStatus);
      } else {
        afetadosAgora.push(ativoComStatus);
      }
    }
  }
  return { afetadosAgora, jaCorrigidos };
}

function criarDestaqueDoCvss(vulnerabilidade) {
  const nivel = vulnerabilidade.nivel;
  return criarElemento("div", { classe: "destaque-do-cvss" }, [
    criarElemento("div", { classe: "numero-de-risco" }, [
      criarElemento("span", {
        classe: "numero-de-risco-valor",
        texto: formatarCvss(vulnerabilidade.cvss),
      }),
      criarElemento("span", { classe: "legenda", texto: "CVSS" }),
    ]),
    criarElemento("span", { classe: "destaque-do-nivel" }, [
      criarElemento("span", { classe: "bolinha", "data-nivel": nivel }),
      criarElemento("span", {
        classe: "nome-do-nivel",
        "data-nivel": nivel,
        texto: NIVEIS_DE_GRAVIDADE[nivel].rotulo,
      }),
    ]),
  ]);
}

function criarSecaoDeAtivos({ titulo, vinculos, opcoes, textoQuandoVazia, apagada }) {
  const lista = criarElemento("ul", {
    classe: apagada ? "lista-de-afetados lista-de-afetados-apagada" : "lista-de-afetados",
  });
  for (const { ativo, statusDeTratamento } of vinculos) {
    const status = encontrarOpcao(opcoes.statusDeTratamento, statusDeTratamento);
    lista.append(
      criarElemento("li", { classe: "item-de-afetado" }, [
        criarElemento("a", { classe: "item-de-dependencia-nome", href: `#/ativos/${ativo.id}` }, [
          criarIcone(iconeDoTipo(ativo.tipo)),
          criarElemento("span", { texto: ativo.nome }),
        ]),
        status ? criarPilulaDeStatus({ rotulo: status.rotulo, cor: status.cor }) : null,
      ]),
    );
  }
  if (vinculos.length === 0) {
    lista.append(
      criarElemento("li", { classe: "texto-de-apoio secao-da-janela-vazia", texto: textoQuandoVazia }),
    );
  }
  return criarElemento("section", { classe: "secao-da-janela" }, [
    criarElemento("h3", { classe: "titulo-de-secao secao-da-janela-titulo", texto: titulo }),
    lista,
  ]);
}

function criarAcoesDaVulnerabilidade(vulnerabilidade, controles) {
  const botaoDeEditar = criarBotao({
    texto: "Editar",
    variacao: "secundario",
    icone: "editar",
    pequeno: true,
    aoClicar: () => navegarPara(`/vulnerabilidades/${vulnerabilidade.id_vulnerabilidade}/editar`),
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
      pergunta: `Excluir ${vulnerabilidade.nome_vulnerabilidade}?`,
      explicacao: "Os vínculos dela com os ativos também serão removidos.",
      aoConfirmar: async () => {
        await excluirVulnerabilidade(vulnerabilidade.id_vulnerabilidade);
        controles.pedirFechamento();
        atualizarTelaAtual();
        mostrarAvisoDeSucesso("Vulnerabilidade excluída");
      },
    });
  });
  return [botaoDeEditar, botaoDeExcluir];
}
