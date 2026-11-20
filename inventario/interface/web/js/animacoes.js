const TEMPO_MAXIMO_DE_TRANSICAO = 450;

export function mostrarComTransicao(elemento) {
  elemento.getBoundingClientRect();
  elemento.setAttribute("data-visivel", "");
}

export function esconderComTransicao(elemento, elementoQueAnima = elemento) {
  return new Promise((resolver) => {
    let terminou = false;

    function terminar() {
      if (terminou) {
        return;
      }
      terminou = true;
      elementoQueAnima.removeEventListener("transitionend", aoTerminarTransicao);
      resolver();
    }

    function aoTerminarTransicao(evento) {
      if (evento.target === elementoQueAnima && evento.propertyName === "opacity") {
        terminar();
      }
    }

    elementoQueAnima.addEventListener("transitionend", aoTerminarTransicao);
    elemento.removeAttribute("data-visivel");
    setTimeout(terminar, TEMPO_MAXIMO_DE_TRANSICAO);
  });
}
