import { criarElemento, gerarIdentificador } from "../elementos.js";
import { criarIcone } from "../icones.js";

export function criarContador({ rotulo, valor = 1, minimo = 1, maximo = 99999, unidade, aoMudar }) {
  let valorAtual = limitar(valor, minimo, maximo);

  const numero = criarElemento("input", {
    type: "text",
    classe: "contador-numero",
    id: gerarIdentificador("contador"),
    role: "spinbutton",
    inputmode: "numeric",
    autocomplete: "off",
    "aria-valuemin": String(minimo),
    "aria-valuemax": String(maximo),
  });
  const botaoDeMenos = criarSinal("menos", `Diminuir ${rotulo.toLowerCase()}`);
  const botaoDeMais = criarSinal("mais", `Aumentar ${rotulo.toLowerCase()}`);
  const pilula = criarElemento("div", { classe: "contador" }, [botaoDeMenos, numero, botaoDeMais]);
  const elemento = criarElemento("div", { classe: "contador-com-unidade" }, [pilula]);
  if (unidade) {
    elemento.append(criarElemento("span", { classe: "contador-unidade", texto: unidade }));
  }

  function mostrarValor() {
    numero.value = String(valorAtual);
    numero.setAttribute("aria-valuenow", String(valorAtual));
    ajustarLarguraDoNumero(numero);
    botaoDeMenos.disabled = valorAtual <= minimo;
    botaoDeMais.disabled = valorAtual >= maximo;
  }

  function definirValor(novoValor) {
    const valorLimitado = limitar(novoValor, minimo, maximo);
    const mudou = valorLimitado !== valorAtual;
    valorAtual = valorLimitado;
    mostrarValor();
    if (mudou && aoMudar) {
      aoMudar(valorAtual);
    }
  }

  botaoDeMenos.addEventListener("click", () => definirValor(valorAtual - 1));
  botaoDeMais.addEventListener("click", () => definirValor(valorAtual + 1));

  numero.addEventListener("focus", () => numero.select());
  numero.addEventListener("click", () => numero.select());
  numero.addEventListener("input", () => {
    numero.value = manterSoDigitos(numero.value);
    ajustarLarguraDoNumero(numero);
  });
  numero.addEventListener("change", () => confirmarDigitacao());
  numero.addEventListener("blur", () => confirmarDigitacao());
  numero.addEventListener("keydown", (evento) => {
    if (evento.key === "ArrowUp") {
      evento.preventDefault();
      definirValor(valorAtual + 1);
    } else if (evento.key === "ArrowDown") {
      evento.preventDefault();
      definirValor(valorAtual - 1);
    } else if (evento.key === "Enter") {
      confirmarDigitacao();
    }
  });

  function confirmarDigitacao() {
    if (numero.value === "") {
      mostrarValor();
      return;
    }
    definirValor(Number(numero.value));
  }

  mostrarValor();
  return { elemento, campo: numero, obterValor: () => valorAtual, definirValor };
}

function criarSinal(nomeDoIcone, rotuloAcessivel) {
  return criarElemento(
    "button",
    { type: "button", classe: "contador-sinal", "aria-label": rotuloAcessivel },
    [criarIcone(nomeDoIcone)],
  );
}

function ajustarLarguraDoNumero(numero) {
  numero.style.width = `${Math.max(2, numero.value.length) + 0.4}ch`;
}

function manterSoDigitos(texto) {
  return texto.replace(/\D/g, "").slice(0, 6);
}

function limitar(valor, minimo, maximo) {
  return Math.max(minimo, Math.min(maximo, Math.round(valor)));
}
