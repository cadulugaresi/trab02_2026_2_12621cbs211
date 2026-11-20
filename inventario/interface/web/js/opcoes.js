import { buscarOpcoes } from "./api.js";
import {
  CORES_DE_IMPRESSORA,
  SETORES,
  STATUS_DE_TRATAMENTO,
  STATUS_DO_ATIVO,
  TECNOLOGIAS_DE_IMPRESSORA,
  TIPOS_DE_ATIVO,
  montarOpcoesDoEnum,
} from "./rotulos.js";

let opcoesCarregando = null;

export function encontrarOpcao(opcoes, valor) {
  for (const opcao of opcoes) {
    if (opcao.valor === valor) {
      return opcao;
    }
  }
  return undefined;
}

export function encontrarValorPeloNome(opcoes, nome) {
  for (const opcao of opcoes) {
    if (opcao.nome === nome) {
      return opcao.valor;
    }
  }
  return null;
}

export function rotuloDaOpcao(opcoes, valor) {
  const opcao = encontrarOpcao(opcoes, valor);
  return opcao ? opcao.rotulo : String(valor);
}

export function carregarOpcoes() {
  if (opcoesCarregando === null) {
    opcoesCarregando = buscarOpcoes()
      .then(converterOpcoesDaApi)
      .catch((erro) => {
        opcoesCarregando = null;
        throw erro;
      });
  }
  return opcoesCarregando;
}

function converterOpcoesDaApi(opcoesDaApi) {
  return {
    tipos: converterTipos(opcoesDaApi.tipos),
    setores: montarOpcoesDoEnum(opcoesDaApi.setores, SETORES),
    statusDoAtivo: montarOpcoesDoEnum(opcoesDaApi.status_do_ativo, STATUS_DO_ATIVO),
    statusDeTratamento: montarOpcoesDoEnum(opcoesDaApi.status_de_tratamento, STATUS_DE_TRATAMENTO),
    coresDeImpressora: montarOpcoesDoEnum(opcoesDaApi.cores, CORES_DE_IMPRESSORA),
    tecnologiasDeImpressora: montarOpcoesDoEnum(opcoesDaApi.tecnologias, TECNOLOGIAS_DE_IMPRESSORA),
  };
}

function converterTipos(tiposDaApi) {
  const tipos = [];
  for (const tipoDaApi of tiposDaApi) {
    const tipoConhecido = TIPOS_DE_ATIVO[tipoDaApi.nome];
    tipos.push({
      valor: tipoDaApi.nome,
      rotulo: tipoConhecido ? tipoConhecido.rotulo : tipoDaApi.nome,
      icone: tipoConhecido ? tipoConhecido.icone : "ativos",
      fatorDeExposicaoPadrao: tipoDaApi.fator_exposicao_padrao,
    });
  }
  return tipos;
}
