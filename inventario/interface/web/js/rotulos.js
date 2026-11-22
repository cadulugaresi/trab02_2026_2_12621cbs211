export const TIPOS_DE_ATIVO = {
  Notebook: { rotulo: "Notebook", icone: "notebook" },
  Servidor: { rotulo: "Servidor", icone: "servidor" },
  Roteador: { rotulo: "Roteador", icone: "roteador" },
  Impressora: { rotulo: "Impressora", icone: "impressora" },
};

export const SETORES = {
  TI: { rotulo: "TI" },
  FINANCEIRO: { rotulo: "Financeiro" },
  MARKETING: { rotulo: "Marketing" },
  RH: { rotulo: "RH" },
  JURIDICO: { rotulo: "Jurídico" },
};

export const STATUS_DO_ATIVO = {
  ATIVO: { rotulo: "Ativo", cor: "verde" },
  EM_MANUTENCAO: { rotulo: "Em manutenção", cor: "amarelo" },
  INATIVO: { rotulo: "Inativo", cor: "vermelho" },
};

export const STATUS_DE_TRATAMENTO = {
  ABERTA: { rotulo: "Aberta", cor: "vermelho" },
  EM_TRATAMENTO: { rotulo: "Em tratamento", cor: "amarelo" },
  CORRIGIDA: { rotulo: "Corrigida", cor: "verde" },
  ACEITA: { rotulo: "Aceita", cor: "cinza" },
};

export const NIVEIS_DE_GRAVIDADE = {
  BAIXO: { rotulo: "Baixo" },
  MEDIO: { rotulo: "Médio" },
  ALTO: { rotulo: "Alto" },
  CRITICO: { rotulo: "Crítico" },
};

export const CORES_DE_IMPRESSORA = {
  COLORIDA: { rotulo: "Colorida" },
  PRETA_E_BRANCA: { rotulo: "Preta e branca" },
};

export const TECNOLOGIAS_DE_IMPRESSORA = {
  TINTA: { rotulo: "Tinta" },
  LASER: { rotulo: "Laser" },
};

export function montarOpcoesDoEnum(opcoesDaApi, rotulosDoEnum) {
  const opcoes = [];
  for (const opcaoDaApi of opcoesDaApi) {
    const rotuloConhecido = rotulosDoEnum[opcaoDaApi.nome];
    opcoes.push({
      valor: opcaoDaApi.valor,
      nome: opcaoDaApi.nome,
      rotulo: rotuloConhecido ? rotuloConhecido.rotulo : opcaoDaApi.nome,
      cor: rotuloConhecido ? rotuloConhecido.cor : undefined,
    });
  }
  return opcoes;
}
