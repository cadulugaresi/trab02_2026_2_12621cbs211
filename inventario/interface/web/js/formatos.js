const FORMATO_DE_UMA_CASA = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

const FORMATO_DE_ATE_DUAS_CASAS = new Intl.NumberFormat("pt-BR", {
  maximumFractionDigits: 2,
});

const FORMATO_DE_DUAS_CASAS = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

export const MENOR_CVSS = 0.1;
export const MAIOR_CVSS = 10;

export function formatarCvss(cvss) {
  return FORMATO_DE_UMA_CASA.format(cvss);
}

export function formatarRisco(valor) {
  return FORMATO_DE_DUAS_CASAS.format(valor);
}

export function formatarFracao(fracao) {
  return FORMATO_DE_DUAS_CASAS.format(fracao);
}

export function formatarNumero(valor) {
  return FORMATO_DE_ATE_DUAS_CASAS.format(valor);
}

export function lerNumeroDigitado(texto) {
  const textoLimpo = texto.trim().replace(",", ".");
  if (textoLimpo === "" || !/^\d*\.?\d*$/.test(textoLimpo) || textoLimpo === ".") {
    return null;
  }
  return Number(textoLimpo);
}

export function arredondarCvss(cvss) {
  return Math.round(cvss * 10) / 10;
}

export function cvssEstaNaFaixa(cvss) {
  const cvssArredondado = arredondarCvss(cvss);
  return cvssArredondado >= MENOR_CVSS && cvssArredondado <= MAIOR_CVSS;
}

export function descobrirNivelPeloCvss(cvss) {
  if (cvss > 8.9) {
    return "CRITICO";
  }
  if (cvss > 6.9) {
    return "ALTO";
  }
  if (cvss > 3.9) {
    return "MEDIO";
  }
  return "BAIXO";
}

export function normalizarParaBusca(texto) {
  return texto.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
}
