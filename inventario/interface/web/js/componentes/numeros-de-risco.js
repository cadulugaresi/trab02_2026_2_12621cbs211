import { criarElemento } from "../elementos.js";
import { formatarRisco } from "../formatos.js";
import { criarNumeroAnimado } from "./numero-animado.js";

const SEM_NUMERO = "—";

export function criarNumerosDeRisco(riscosIniciais) {
  const valores = riscosIniciais ?? { proprio: 0, herdado: 0, efetivo: 0 };
  const proprio = criarNumeroDeRisco("Risco próprio", valores.proprio);
  const herdado = criarNumeroDeRisco("Risco herdado", valores.herdado);
  const efetivo = criarNumeroDeRisco("Risco efetivo", valores.efetivo);
  const aviso = criarElemento("p", { classe: "texto-de-apoio aviso-dos-riscos", hidden: true });
  const elemento = criarElemento("div", { classe: "bloco-de-riscos" }, [
    criarElemento("div", { classe: "numeros-de-risco" }, [
      proprio.elemento,
      herdado.elemento,
      efetivo.elemento,
    ]),
    aviso,
  ]);

  function animarAte(novosRiscos) {
    aviso.hidden = true;
    proprio.numero.animarAte(novosRiscos.proprio);
    herdado.numero.animarAte(novosRiscos.herdado);
    efetivo.numero.animarAte(novosRiscos.efetivo);
  }

  function mostrarIndisponivel(mensagem) {
    for (const numeroDeRisco of [proprio, herdado, efetivo]) {
      numeroDeRisco.numero.mostrarTexto(SEM_NUMERO);
    }
    aviso.textContent = mensagem;
    aviso.hidden = false;
  }

  if (riscosIniciais === null) {
    mostrarIndisponivel("");
  }
  return { elemento, animarAte, mostrarIndisponivel };
}

function criarNumeroDeRisco(rotulo, valorInicial) {
  const numero = criarNumeroAnimado({
    valor: valorInicial,
    formatar: formatarRisco,
    classe: "numero-de-risco-valor",
  });
  const elemento = criarElemento("div", { classe: "numero-de-risco" }, [
    numero.elemento,
    criarElemento("span", { classe: "legenda", texto: rotulo }),
  ]);
  return { elemento, numero };
}
