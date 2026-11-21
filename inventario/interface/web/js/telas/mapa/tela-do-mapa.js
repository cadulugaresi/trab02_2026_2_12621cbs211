import { listarAtivos } from "../../api.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarElemento } from "../../elementos.js";
import { carregarOpcoes } from "../../opcoes.js";
import { buscarRanking } from "../../riscos.js";
import { navegarPara } from "../../roteador.js";
import { criarCabecalhoDeAtivos } from "../ativos/cabecalho-de-ativos.js";
import {
  criarFiltrosDeAtivos,
  existeFiltroDeAtivos,
  lerFiltrosDeAtivos,
} from "../ativos/filtros-de-ativos.js";
import { criarEstadoVazio, descreverQuantidade } from "../estados-da-lista.js";
import { centralizarCamera, permitirArrastarOMapa } from "./arrastar-o-mapa.js";
import { contarLigacoesVisiveis, escolherAtivosVisiveis } from "./ativos-visiveis.js";
import { criarDesenhoDoMapa } from "./desenho-do-mapa.js";
import { animarChegadaDoMapa, receberMapaPuxado } from "./mapa-puxado.js";
import { medirMapa, podeArrastar } from "./medidas-do-mapa.js";
import { calcularPosicoesDoMapa } from "./posicoes-do-mapa.js";
import { QUANTIDADE_DE_MAIORES_RISCOS } from "./riscos-do-mapa.js";

const ESPERA_AO_REDIMENSIONAR = 150;
const ESPERA_DA_BUSCA = 250;
const EXPLICACAO_SEM_RANKING =
  "Por isso, as bolinhas ficam do mesmo tamanho e sem a marca dos maiores riscos.";
const EXPLICACAO_DO_TAMANHO = "O tamanho da bolinha cresce com o risco efetivo.";
const EXPLICACAO_DA_MARCA =
  `Os ${QUANTIDADE_DE_MAIORES_RISCOS} maiores riscos do ranking, com a posição de cada um.`;
const EXPLICACAO_DAS_SETAS = "As setas vão de quem depende para o ativo do qual depende.";
const EXPLICACAO_DA_BUSCA =
  "Ao buscar um nome, o mapa mostra o ativo encontrado (com contorno preto) e só as dependências dele.";
const DICA_DE_ARRASTAR_NO_COMPUTADOR = "Arraste o fundo do mapa para ver o resto.";
const DICA_DE_ARRASTAR_NO_CELULAR = "Deslize o mapa para os lados para ver o resto.";

export function montarTelaDoMapa(tela) {
  const filtros = lerFiltrosDeAtivos();
  const contagem = criarElemento("p", {
    classe: "texto-de-apoio contagem-da-tela",
    "aria-live": "polite",
  });
  const cabecalho = criarCabecalhoDeAtivos({ modo: "mapa", contagem: contagem });
  const faixa = criarFaixaDeErro();
  const areaDosFiltros = criarElemento("div", { classe: "filtros-da-lista" });
  const avisoSemRanking = criarElemento("p", { classe: "aviso-do-mapa", hidden: true });
  const areaDoMapa = criarElemento("div", { classe: "area-do-mapa", "aria-busy": "true" });
  const dicaDeArrastar = criarElemento("p", { classe: "dica-do-mapa", hidden: true });
  const legenda = criarLegendaDoMapa(dicaDeArrastar);
  let dados = null;
  let controlesDosFiltros = null;
  let posicoes = null;
  let chaveDasPosicoes = null;
  let camera = null;
  let larguraDesenhada = 0;
  let temporizadorDoRedimensionamento = null;
  let temporizadorDaBusca = null;

  tela.append(cabecalho, faixa.elemento, areaDosFiltros, avisoSemRanking, areaDoMapa, legenda);

  function montarFiltros(opcoes) {
    if (controlesDosFiltros !== null) {
      return;
    }
    controlesDosFiltros = criarFiltrosDeAtivos({
      opcoes: opcoes,
      filtros: filtros,
      textoDaBusca: "Buscar ativo e ver as dependências dele",
      aoMudar: redesenharComOsFiltros,
      aoDigitarNaBusca: () => {
        clearTimeout(temporizadorDaBusca);
        temporizadorDaBusca = setTimeout(redesenharComOsFiltros, ESPERA_DA_BUSCA);
      },
    });
    areaDosFiltros.append(controlesDosFiltros.elemento);
  }

  function redesenharComOsFiltros() {
    if (dados !== null) {
      desenhar();
    }
  }

  function limparFiltros() {
    controlesDosFiltros.limpar();
    redesenharComOsFiltros();
  }

  function prepararPosicoes(ativosVisiveis, medidas) {
    const proporcao = medidas.desenho.largura / medidas.desenho.altura;
    const identificadores = [];
    for (const ativo of ativosVisiveis) {
      identificadores.push(ativo.id);
    }
    const chave = `${identificadores.join(",")}|${proporcao}`;
    if (chave === chaveDasPosicoes) {
      return;
    }
    posicoes = calcularPosicoesDoMapa(ativosVisiveis, proporcao);
    chaveDasPosicoes = chave;
    camera = null;
  }

  async function carregar() {
    try {
      montarFiltros(await carregarOpcoes());
      const ativos = await listarAtivos();
      const { ranking, mensagem } = await buscarRanking();
      faixa.esconder();
      dados = { ativos, ranking, mensagem };
      chaveDasPosicoes = null;
      desenhar();
    } catch (erro) {
      faixa.mostrar(erro.message);
      areaDoMapa.removeAttribute("aria-busy");
    }
  }

  function desenhar() {
    areaDoMapa.removeAttribute("aria-busy");
    const { ativos: ativosVisiveis, buscados } = escolherAtivosVisiveis(dados.ativos, filtros);
    contagem.textContent = descreverConteudo(dados.ativos, ativosVisiveis, buscados, filtros);
    avisoSemRanking.hidden = dados.ranking !== null;
    avisoSemRanking.textContent = `${dados.mensagem} ${EXPLICACAO_SEM_RANKING}`;
    legenda.hidden = ativosVisiveis.length === 0;
    areaDosFiltros.hidden = dados.ativos.length === 0;

    if (dados.ativos.length === 0) {
      areaDoMapa.replaceChildren(criarMapaVazio());
      return null;
    }
    if (ativosVisiveis.length === 0) {
      areaDoMapa.replaceChildren(criarMapaSemResultado(limparFiltros));
      return null;
    }

    larguraDesenhada = areaDoMapa.clientWidth;
    const medidas = medirMapa(larguraDesenhada, ativosVisiveis.length);
    prepararPosicoes(ativosVisiveis, medidas);
    const desenho = criarDesenhoDoMapa({
      ativos: ativosVisiveis,
      ranking: dados.ranking,
      posicoes: posicoes,
      largura: medidas.desenho.largura,
      altura: medidas.desenho.altura,
      estreito: medidas.ehCelular,
      buscados: buscados,
    });
    const arrastavel = podeArrastar(medidas);
    dicaDeArrastar.hidden = !arrastavel;
    dicaDeArrastar.textContent = medidas.ehCelular
      ? DICA_DE_ARRASTAR_NO_CELULAR
      : DICA_DE_ARRASTAR_NO_COMPUTADOR;
    if (arrastavel) {
      if (camera === null) {
        camera = centralizarCamera(medidas);
      }
      permitirArrastarOMapa({ desenho, medidas, camera });
    }
    areaDoMapa.replaceChildren(desenho);
    return { desenho, medidas };
  }

  function redesenharSeALarguraMudou() {
    clearTimeout(temporizadorDoRedimensionamento);
    temporizadorDoRedimensionamento = setTimeout(() => {
      if (dados !== null && areaDoMapa.clientWidth !== larguraDesenhada) {
        desenhar();
      }
    }, ESPERA_AO_REDIMENSIONAR);
  }

  window.addEventListener("resize", redesenharSeALarguraMudou);

  const mapaPuxado = receberMapaPuxado();
  if (mapaPuxado === null) {
    carregar();
  } else {
    carregarOpcoes().then(montarFiltros);
    dados = {
      ativos: mapaPuxado.ativos,
      ranking: mapaPuxado.ranking,
      mensagem: mapaPuxado.mensagem,
    };
    const resultado = desenhar();
    if (resultado !== null) {
      requestAnimationFrame(() => {
        animarChegadaDoMapa({
          desenho: resultado.desenho,
          retanguloDeOrigem: recortarParteVisivel(mapaPuxado.retangulo, resultado.medidas, camera),
          elementosEmVolta: [cabecalho, areaDosFiltros, legenda],
        });
      });
    }
  }

  return {
    atualizar: carregar,
    desmontar: () => {
      clearTimeout(temporizadorDoRedimensionamento);
      clearTimeout(temporizadorDaBusca);
      window.removeEventListener("resize", redesenharSeALarguraMudou);
    },
  };
}

function recortarParteVisivel(retanguloDaPrevia, medidas, camera) {
  if (camera === null) {
    return retanguloDaPrevia;
  }
  const escalaX = retanguloDaPrevia.width / medidas.desenho.largura;
  const escalaY = retanguloDaPrevia.height / medidas.desenho.altura;
  return {
    left: retanguloDaPrevia.left + camera.x * escalaX,
    top: retanguloDaPrevia.top + camera.y * escalaY,
    width: medidas.visivel.largura * escalaX,
    height: medidas.visivel.altura * escalaY,
  };
}

function descreverConteudo(todosOsAtivos, ativosVisiveis, buscados, filtros) {
  const textoDasDependencias = descreverQuantidade(
    contarLigacoesVisiveis(ativosVisiveis, buscados),
    "dependência",
    "dependências",
  );
  if (!existeFiltroDeAtivos(filtros)) {
    const textoDosAtivos = descreverQuantidade(todosOsAtivos.length, "ativo", "ativos");
    return `${textoDosAtivos} · ${textoDasDependencias}`;
  }
  return `${ativosVisiveis.length} de ${todosOsAtivos.length} ativos · ${textoDasDependencias}`;
}

function criarMapaVazio() {
  return criarElemento("ul", {}, [
    criarEstadoVazio({
      titulo: "Nenhum ativo para mostrar",
      explicacao: "Cadastre ativos e as dependências entre eles para ver o mapa.",
      textoDoBotao: "Cadastrar o primeiro ativo",
      aoClicar: () => navegarPara("/ativos/novo"),
    }),
  ]);
}

function criarMapaSemResultado(limparFiltros) {
  return criarElemento("ul", {}, [
    criarEstadoVazio({
      titulo: "Nenhum ativo com esses filtros",
      explicacao: "Tente outro nome ou tire um dos filtros.",
      textoDoBotao: "Limpar filtros",
      variacao: "secundario",
      aoClicar: limparFiltros,
    }),
  ]);
}

function criarLegendaDoMapa(dicaDeArrastar) {
  return criarElemento("div", { classe: "legenda-do-mapa" }, [
    dicaDeArrastar,
    criarElemento("p", { texto: EXPLICACAO_DO_TAMANHO }),
    criarElemento("p", { classe: "legenda-do-mapa-maiores-riscos" }, [
      criarElemento("span", {
        classe: "amostra-da-marca-de-maior-risco",
        "aria-hidden": "true",
        texto: "1",
      }),
      criarElemento("span", { texto: EXPLICACAO_DA_MARCA }),
    ]),
    criarElemento("p", { texto: EXPLICACAO_DAS_SETAS }),
    criarElemento("p", { texto: EXPLICACAO_DA_BUSCA }),
  ]);
}
