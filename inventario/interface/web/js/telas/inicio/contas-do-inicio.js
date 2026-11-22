import { encontrarValorPeloNome } from "../../opcoes.js";

const NIVEIS_DO_MAIS_GRAVE_AO_MAIS_LEVE = ["CRITICO", "ALTO", "MEDIO", "BAIXO"];
const NIVEIS_DOS_SETORES = ["CRITICO", "ALTO"];
const ORDEM_DA_MEIA_LUA = ["CORRIGIDA", "EM_TRATAMENTO", "ACEITA", "ABERTA"];

const ADJETIVOS_DOS_NIVEIS = {
  CRITICO: { singular: "crítica", plural: "críticas" },
  ALTO: { singular: "alta", plural: "altas" },
  MEDIO: { singular: "média", plural: "médias" },
  BAIXO: { singular: "baixa", plural: "baixas" },
};

export function montarResumoDoInicio({ ativos, vulnerabilidades, opcoes }) {
  const valorDaCorrigida = encontrarValorPeloNome(opcoes.statusDeTratamento, "CORRIGIDA");
  const vinculos = listarVinculos(ativos, vulnerabilidades);
  const vinculosAbertos = [];
  for (const vinculo of vinculos) {
    if (vinculo.status !== valorDaCorrigida) {
      vinculosAbertos.push(vinculo);
    }
  }
  const abertasPorNivel = contarPorNivel(vinculosAbertos);
  const vinculosPorStatus = contarVinculosPorStatus(vinculos, opcoes.statusDeTratamento);

  return {
    numeros: {
      ativos: ativos.length,
      abertas: vinculosAbertos.length,
      criticasAbertas: abertasPorNivel.CRITICO,
      emManutencao: contarAtivosEmManutencao(ativos, opcoes.statusDoAtivo),
    },
    frase: escreverFraseDoMaisUrgente(abertasPorNivel),
    vinculosPorStatus: vinculosPorStatus,
    totalDeVinculos: vinculos.length,
    porcentagemDeCorrigidas: calcularPorcentagemDeCorrigidas(vinculosPorStatus, vinculos.length),
    setores: contarCriticasEAltasPorSetor(vinculosAbertos, opcoes.setores),
  };
}

function listarVinculos(ativos, vulnerabilidades) {
  const vulnerabilidadesPorId = new Map();
  for (const vulnerabilidade of vulnerabilidades) {
    vulnerabilidadesPorId.set(vulnerabilidade.id_vulnerabilidade, vulnerabilidade);
  }
  const vinculos = [];
  for (const ativo of ativos) {
    for (const vinculo of ativo.vulnerabilidades) {
      const vulnerabilidade = vulnerabilidadesPorId.get(vinculo.id_vulnerabilidade);
      if (vulnerabilidade) {
        vinculos.push({ ativo, nivel: vulnerabilidade.nivel, status: vinculo.status_tratamento });
      }
    }
  }
  return vinculos;
}

function contarPorNivel(vinculos) {
  const quantidades = { CRITICO: 0, ALTO: 0, MEDIO: 0, BAIXO: 0 };
  for (const vinculo of vinculos) {
    quantidades[vinculo.nivel] += 1;
  }
  return quantidades;
}

function contarAtivosEmManutencao(ativos, statusDoAtivo) {
  const valorEmManutencao = encontrarValorPeloNome(statusDoAtivo, "EM_MANUTENCAO");
  let quantidade = 0;
  for (const ativo of ativos) {
    if (ativo.status === valorEmManutencao) {
      quantidade += 1;
    }
  }
  return quantidade;
}

function escreverFraseDoMaisUrgente(abertasPorNivel) {
  for (const nivel of NIVEIS_DO_MAIS_GRAVE_AO_MAIS_LEVE) {
    const quantidade = abertasPorNivel[nivel];
    if (quantidade > 0) {
      return {
        quantidade: quantidade,
        texto: descreverAbertas(quantidade, nivel),
        complemento: nivel === "CRITICO" ? "" : "Nenhuma vulnerabilidade crítica aberta",
      };
    }
  }
  return { quantidade: null, texto: "Nenhuma vulnerabilidade aberta", complemento: "" };
}

function descreverAbertas(quantidade, nivel) {
  const adjetivo = ADJETIVOS_DOS_NIVEIS[nivel];
  if (quantidade === 1) {
    return `vulnerabilidade ${adjetivo.singular} aberta`;
  }
  return `vulnerabilidades ${adjetivo.plural} abertas`;
}

function contarVinculosPorStatus(vinculos, opcoesDeStatus) {
  const contagens = [];
  for (const nome of ORDEM_DA_MEIA_LUA) {
    const valor = encontrarValorPeloNome(opcoesDeStatus, nome);
    let quantidade = 0;
    for (const vinculo of vinculos) {
      if (vinculo.status === valor) {
        quantidade += 1;
      }
    }
    contagens.push({ opcao: encontrarOpcaoPeloNome(opcoesDeStatus, nome), quantidade });
  }
  return contagens;
}

function encontrarOpcaoPeloNome(opcoes, nome) {
  for (const opcao of opcoes) {
    if (opcao.nome === nome) {
      return opcao;
    }
  }
  return { nome: nome, rotulo: nome, cor: "cinza" };
}

function calcularPorcentagemDeCorrigidas(vinculosPorStatus, totalDeVinculos) {
  if (totalDeVinculos === 0) {
    return null;
  }
  for (const contagem of vinculosPorStatus) {
    if (contagem.opcao.nome === "CORRIGIDA") {
      return Math.round((contagem.quantidade / totalDeVinculos) * 100);
    }
  }
  return 0;
}

function contarCriticasEAltasPorSetor(vinculosAbertos, opcoesDeSetor) {
  const setores = [];
  for (const opcao of opcoesDeSetor) {
    let quantidade = 0;
    for (const vinculo of vinculosAbertos) {
      if (vinculo.ativo.setor === opcao.valor && NIVEIS_DOS_SETORES.includes(vinculo.nivel)) {
        quantidade += 1;
      }
    }
    setores.push({ opcao, quantidade, destaque: null });
  }
  setores.sort((primeiro, segundo) => segundo.quantidade - primeiro.quantidade);
  marcarPiorEMaisSeguro(setores);
  return setores;
}

function marcarPiorEMaisSeguro(setores) {
  if (setores.length < 2) {
    return;
  }
  const pior = setores[0];
  const maisSeguro = setores[setores.length - 1];
  if (pior.quantidade === maisSeguro.quantidade) {
    return;
  }
  pior.destaque = "pior";
  maisSeguro.destaque = "mais-seguro";
}
