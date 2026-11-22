import { formatarNumero } from "../../formatos.js";
import { rotuloDaOpcao } from "../../opcoes.js";
import { TIPOS_DE_ATIVO } from "../../rotulos.js";

export function iconeDoTipo(tipo) {
  const tipoConhecido = TIPOS_DE_ATIVO[tipo];
  return tipoConhecido ? tipoConhecido.icone : "ativos";
}

export function rotuloDoTipo(tipo) {
  const tipoConhecido = TIPOS_DE_ATIVO[tipo];
  return tipoConhecido ? tipoConhecido.rotulo : tipo;
}

export function descreverAtivo(ativo, opcoes) {
  return [
    rotuloDoTipo(ativo.tipo),
    rotuloDaOpcao(opcoes.setores, ativo.setor),
    ativo.responsavel,
  ].join(" · ");
}

export function descreverCamposDoTipo(ativo, opcoes) {
  if (ativo.tipo === "Notebook") {
    return [ativo.sistema_operacional, `Tela de ${formatarNumero(ativo.tela)} polegadas`];
  }
  if (ativo.tipo === "Servidor") {
    return [
      `${ativo.ram} GB de RAM`,
      `${formatarNumero(ativo.armazenamento)} TB de armazenamento`,
    ];
  }
  if (ativo.tipo === "Roteador") {
    return [`${ativo.portas} portas`, `${ativo.velocidade} MB de velocidade`];
  }
  if (ativo.tipo === "Impressora") {
    return [
      rotuloDaOpcao(opcoes.coresDeImpressora, ativo.cor),
      rotuloDaOpcao(opcoes.tecnologiasDeImpressora, ativo.tecnologia),
    ];
  }
  return [];
}

export function indexarAtivosPorId(ativos) {
  const ativosPorId = new Map();
  for (const ativo of ativos) {
    ativosPorId.set(ativo.id, ativo);
  }
  return ativosPorId;
}
