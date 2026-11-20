import { buscarNaFila, ehErroDeDemora } from "./conexao.js";

const MENSAGEM_SEM_CONEXAO =
  "Não foi possível falar com o servidor. Confira se a API está rodando e tente de novo.";
const MENSAGEM_DE_DEMORA = "O servidor demorou demais para responder. Tente de novo.";

export class ErroDaApi extends Error {
  constructor(mensagem, status) {
    super(mensagem);
    this.name = "ErroDaApi";
    this.status = status;
  }
}

async function requisitar(metodo, caminho, corpo) {
  const opcoes = { method: metodo, headers: { Accept: "application/json" } };
  if (corpo !== undefined) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }

  let resposta;
  try {
    resposta = await buscarNaFila(caminho, opcoes);
  } catch (erro) {
    throw new ErroDaApi(ehErroDeDemora(erro) ? MENSAGEM_DE_DEMORA : MENSAGEM_SEM_CONEXAO, 0);
  }

  if (resposta.status === 204) {
    return null;
  }
  const dados = await lerCorpoEmJson(resposta);
  if (!resposta.ok) {
    throw new ErroDaApi(descobrirMensagemDoErro(dados, resposta.status), resposta.status);
  }
  return dados;
}

async function lerCorpoEmJson(resposta) {
  try {
    return await resposta.json();
  } catch {
    return null;
  }
}

function descobrirMensagemDoErro(dados, status) {
  if (dados !== null && typeof dados.erro === "string") {
    return dados.erro;
  }
  return `O servidor respondeu com um erro inesperado (código ${status}).`;
}

function montarCaminhoComFiltros(caminho, filtros) {
  const parametros = new URLSearchParams();
  for (const [nome, valor] of Object.entries(filtros)) {
    if (valor !== undefined && valor !== null && valor !== "") {
      parametros.set(nome, valor);
    }
  }
  const textoDosParametros = parametros.toString();
  if (textoDosParametros === "") {
    return caminho;
  }
  return `${caminho}?${textoDosParametros}`;
}

export function verificarSaude() {
  return requisitar("GET", "/saude");
}

export function buscarOpcoes() {
  return requisitar("GET", "/opcoes");
}

export function listarAtivos(filtros = {}) {
  return requisitar("GET", montarCaminhoComFiltros("/ativos", filtros));
}

export function buscarAtivo(idAtivo) {
  return requisitar("GET", `/ativos/${idAtivo}`);
}

export function cadastrarAtivo(dadosDoAtivo) {
  return requisitar("POST", "/ativos", dadosDoAtivo);
}

export function editarAtivo(idAtivo, dadosDoAtivo) {
  return requisitar("PUT", `/ativos/${idAtivo}`, dadosDoAtivo);
}

export function excluirAtivo(idAtivo) {
  return requisitar("DELETE", `/ativos/${idAtivo}`);
}

export function listarVulnerabilidadesDoAtivo(idAtivo) {
  return requisitar("GET", `/ativos/${idAtivo}/vulnerabilidades`);
}

export function vincularVulnerabilidade(idAtivo, idVulnerabilidade, statusDeTratamento) {
  return requisitar("POST", `/ativos/${idAtivo}/vulnerabilidades`, {
    id_vulnerabilidade: idVulnerabilidade,
    status_tratamento: statusDeTratamento,
  });
}

export function atualizarStatusDoVinculo(idAtivo, idVulnerabilidade, statusDeTratamento) {
  return requisitar("PUT", `/ativos/${idAtivo}/vulnerabilidades/${idVulnerabilidade}`, {
    status_tratamento: statusDeTratamento,
  });
}

export function desvincularVulnerabilidade(idAtivo, idVulnerabilidade) {
  return requisitar("DELETE", `/ativos/${idAtivo}/vulnerabilidades/${idVulnerabilidade}`);
}

export function listarDependenciasDoAtivo(idAtivo) {
  return requisitar("GET", `/ativos/${idAtivo}/dependencias`);
}

export function cadastrarDependencia(idAtivo, idAtivoDoQualDepende, fracao) {
  return requisitar("POST", `/ativos/${idAtivo}/dependencias`, {
    id_ativo_do_qual_depende: idAtivoDoQualDepende,
    fracao: fracao,
  });
}

export function atualizarDependencia(idAtivo, idAtivoDoQualDepende, novosDados) {
  return requisitar("PUT", `/ativos/${idAtivo}/dependencias/${idAtivoDoQualDepende}`, novosDados);
}

export function removerDependencia(idAtivo, idAtivoDoQualDepende) {
  return requisitar("DELETE", `/ativos/${idAtivo}/dependencias/${idAtivoDoQualDepende}`);
}

export function listarVulnerabilidades() {
  return requisitar("GET", "/vulnerabilidades");
}

export function buscarVulnerabilidade(idVulnerabilidade) {
  return requisitar("GET", `/vulnerabilidades/${idVulnerabilidade}`);
}

export function cadastrarVulnerabilidade(nomeDaVulnerabilidade, cvss) {
  return requisitar("POST", "/vulnerabilidades", {
    nome_vulnerabilidade: nomeDaVulnerabilidade,
    cvss: cvss,
  });
}

export function editarVulnerabilidade(idVulnerabilidade, novosDados) {
  return requisitar("PUT", `/vulnerabilidades/${idVulnerabilidade}`, novosDados);
}

export function excluirVulnerabilidade(idVulnerabilidade) {
  return requisitar("DELETE", `/vulnerabilidades/${idVulnerabilidade}`);
}

export function listarRiscos() {
  return requisitar("GET", "/riscos");
}
