import { criarElemento, gerarIdentificador } from "../elementos.js";
import {
  arredondarCvss,
  cvssEstaNaFaixa,
  descobrirNivelPeloCvss,
  formatarCvss,
  lerNumeroDigitado,
} from "../formatos.js";
import { NIVEIS_DE_GRAVIDADE } from "../rotulos.js";
import { mostrarAjuda } from "./campos.js";

export const AJUDA_DO_CVSS = "Nota de 0,1 a 10. Quanto maior, mais grave";
const AVISO_DE_CVSS_FORA_DA_FAIXA = "Use de 0,1 a 10";
export const EXPLICACAO_DO_CVSS =
  "O CVSS (Common Vulnerability Scoring System) é a nota de gravidade de uma vulnerabilidade. " +
  "Até 3,9 é baixa, de 4,0 a 6,9 é média, de 7,0 a 8,9 é alta e acima de 8,9 é crítica.";

export function criarCampoDeCvss({ valor = null, aoMudar }) {
  const campo = criarElemento("input", {
    type: "text",
    classe: "campo campo-cvss",
    id: gerarIdentificador("cvss"),
    inputmode: "decimal",
    placeholder: "0,0",
    autocomplete: "off",
    maxlength: "4",
  });
  const nomeDoNivel = criarElemento("span", { classe: "nome-do-nivel", "aria-live": "polite" });
  const elemento = criarElemento("div", { classe: "campo-de-cvss" }, [campo, nomeDoNivel]);
  let textoDeAjuda = null;
  let cvssAtual = null;

  function atualizar() {
    const numeroDigitado = lerNumeroDigitado(campo.value);
    const campoVazio = campo.value.trim() === "";
    const dentroDaFaixa = numeroDigitado !== null && cvssEstaNaFaixa(numeroDigitado);
    cvssAtual = dentroDaFaixa ? arredondarCvss(numeroDigitado) : null;

    if (cvssAtual === null) {
      campo.removeAttribute("data-nivel");
      nomeDoNivel.removeAttribute("data-nivel");
      nomeDoNivel.textContent = "";
    } else {
      const nivel = descobrirNivelPeloCvss(cvssAtual);
      campo.setAttribute("data-nivel", nivel);
      nomeDoNivel.setAttribute("data-nivel", nivel);
      nomeDoNivel.textContent = NIVEIS_DE_GRAVIDADE[nivel].rotulo;
    }

    const foraDaFaixa = !campoVazio && !dentroDaFaixa;
    if (foraDaFaixa) {
      campo.setAttribute("aria-invalid", "true");
    } else {
      campo.removeAttribute("aria-invalid");
    }
    if (textoDeAjuda !== null) {
      mostrarAjuda(
        textoDeAjuda,
        foraDaFaixa ? AVISO_DE_CVSS_FORA_DA_FAIXA : AJUDA_DO_CVSS,
        foraDaFaixa,
      );
    }
    if (aoMudar) {
      aoMudar(cvssAtual);
    }
  }

  function ligarTextoDeAjuda(novoTextoDeAjuda) {
    textoDeAjuda = novoTextoDeAjuda;
    atualizar();
  }

  function definirValor(novoCvss) {
    campo.value = novoCvss === null ? "" : formatarCvss(novoCvss);
    atualizar();
  }

  campo.addEventListener("input", atualizar);
  campo.addEventListener("blur", () => {
    if (cvssAtual !== null) {
      campo.value = formatarCvss(cvssAtual);
    }
  });

  definirValor(valor);
  return { elemento, campo, obterValor: () => cvssAtual, definirValor, ligarTextoDeAjuda };
}
