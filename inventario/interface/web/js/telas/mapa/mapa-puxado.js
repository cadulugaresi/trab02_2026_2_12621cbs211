let mapaPuxado = null;

export function entregarMapaPuxado(dados) {
  mapaPuxado = dados;
}

export function receberMapaPuxado() {
  const dados = mapaPuxado;
  mapaPuxado = null;
  return dados;
}

export function animarChegadaDoMapa({ desenho, retanguloDeOrigem, elementosEmVolta }) {
  const duracao = lerDuracaoDoMapa();
  if (duracao === 0) {
    return;
  }
  const destino = desenho.getBoundingClientRect();
  if (destino.width === 0) {
    return;
  }
  const escala = retanguloDeOrigem.width / destino.width;
  const deslocamentoX = retanguloDeOrigem.left - destino.left;
  const deslocamentoY = retanguloDeOrigem.top - destino.top;

  desenho.animate(
    [
      { transform: `translate(${deslocamentoX}px, ${deslocamentoY}px) scale(${escala})` },
      { transform: "translate(0, 0) scale(1)" },
    ],
    { duration: duracao, easing: lerCurvaDeMovimento() },
  );
  for (const elemento of elementosEmVolta) {
    elemento.animate([{ opacity: 0 }, { opacity: 1 }], {
      duration: duracao * 0.6,
      delay: duracao * 0.4,
      easing: "ease-out",
      fill: "backwards",
    });
  }
}

function lerDuracaoDoMapa() {
  const valor = getComputedStyle(document.documentElement).getPropertyValue("--duracao-do-mapa");
  return Number.parseFloat(valor) || 0;
}

function lerCurvaDeMovimento() {
  const valor = getComputedStyle(document.documentElement).getPropertyValue("--curva-de-movimento");
  return valor.trim() || "ease-in-out";
}
