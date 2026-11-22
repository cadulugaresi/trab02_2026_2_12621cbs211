import { buscarNaFila } from "./conexao.js";

const PASTA_DOS_ICONES = "/web/icones";

const ARQUIVOS_DOS_ICONES = {
  inicio: "gauge",
  ativos: "monitor-smartphone",
  vulnerabilidades: "bug",
  vinculos: "cable",
  ranking: "list-ordered",
  notebook: "laptop",
  servidor: "server",
  roteador: "router",
  impressora: "printer",
  mais: "plus",
  menos: "minus",
  fechar: "x",
  setaParaBaixo: "chevron-down",
  setaParaEsquerda: "chevron-left",
  setaParaDireita: "chevron-right",
  voltar: "arrow-left",
  avancar: "arrow-right",
  buscar: "search",
  informacao: "info",
  confirmado: "check",
  editar: "pencil",
  excluir: "trash-2",
  abrirPainel: "panel-left",
  menu: "menu",
  alerta: "circle-alert",
};

const iconesCarregados = new Map();

export async function carregarIcones() {
  const carregamentos = [];
  for (const [nome, arquivo] of Object.entries(ARQUIVOS_DOS_ICONES)) {
    carregamentos.push(carregarIcone(nome, arquivo));
  }
  await Promise.all(carregamentos);
}

export function criarIcone(nome, classeExtra = "") {
  const modelo = iconesCarregados.get(nome);
  const icone = modelo ? modelo.cloneNode(true) : criarIconeVazio();
  icone.setAttribute("class", `icone ${classeExtra}`.trim());
  icone.setAttribute("aria-hidden", "true");
  icone.setAttribute("focusable", "false");
  return icone;
}

async function carregarIcone(nome, arquivo) {
  try {
    const resposta = await buscarNaFila(`${PASTA_DOS_ICONES}/${arquivo}.svg`);
    const texto = await resposta.text();
    const documento = new DOMParser().parseFromString(texto, "image/svg+xml");
    const svg = documento.documentElement;
    if (!resposta.ok || svg.nodeName !== "svg") {
      throw new Error(`Ícone ${arquivo} indisponível`);
    }
    svg.removeAttribute("width");
    svg.removeAttribute("height");
    iconesCarregados.set(nome, document.importNode(svg, true));
  } catch {
    iconesCarregados.set(nome, criarIconeVazio());
  }
}

function criarIconeVazio() {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 24 24");
  return svg;
}
