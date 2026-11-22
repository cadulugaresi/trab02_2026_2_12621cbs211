const DISTANCIA_PARA_COMECAR_A_ARRASTAR = 4;
const FOLGA_PARA_MOSTRAR_O_ATIVO_FOCADO = 60;

export function permitirArrastarOMapa({ desenho, medidas, camera }) {
  const visivel = medidas.visivel;
  const limiteX = medidas.desenho.largura - visivel.largura;
  const limiteY = medidas.desenho.altura - visivel.altura;
  let gesto = null;
  let quadroAgendado = null;
  let acabouDeArrastar = false;

  function mostrarCamera() {
    desenho.setAttribute(
      "viewBox",
      `${camera.x} ${camera.y} ${visivel.largura} ${visivel.altura}`,
    );
  }

  function agendarDesenho() {
    if (quadroAgendado !== null) {
      return;
    }
    quadroAgendado = requestAnimationFrame(() => {
      quadroAgendado = null;
      mostrarCamera();
    });
  }

  function moverCameraPara(x, y) {
    camera.x = limitar(x, 0, limiteX);
    camera.y = limitar(y, 0, limiteY);
  }

  function comecar(evento) {
    if (!evento.isPrimary || evento.button !== 0) {
      return;
    }
    if (evento.pointerType === "mouse") {
      evento.preventDefault();
    }
    gesto = {
      id: evento.pointerId,
      x: evento.clientX,
      y: evento.clientY,
      cameraX: camera.x,
      cameraY: camera.y,
      unidadesPorPixel: visivel.largura / desenho.getBoundingClientRect().width,
      arrastando: false,
    };
  }

  function mover(evento) {
    if (gesto === null || evento.pointerId !== gesto.id) {
      return;
    }
    const deslocamentoX = evento.clientX - gesto.x;
    const deslocamentoY = evento.clientY - gesto.y;
    if (!gesto.arrastando) {
      if (Math.hypot(deslocamentoX, deslocamentoY) < DISTANCIA_PARA_COMECAR_A_ARRASTAR) {
        return;
      }
      gesto.arrastando = true;
      desenho.setPointerCapture(evento.pointerId);
      desenho.classList.add("mapa-sendo-arrastado");
    }
    moverCameraPara(
      gesto.cameraX - deslocamentoX * gesto.unidadesPorPixel,
      gesto.cameraY - deslocamentoY * gesto.unidadesPorPixel,
    );
    agendarDesenho();
  }

  function terminar(evento) {
    if (gesto === null || evento.pointerId !== gesto.id) {
      return;
    }
    acabouDeArrastar = gesto.arrastando;
    gesto = null;
    desenho.classList.remove("mapa-sendo-arrastado");
  }

  function impedirCliqueDepoisDeArrastar(evento) {
    if (acabouDeArrastar) {
      evento.preventDefault();
      evento.stopPropagation();
    }
    acabouDeArrastar = false;
  }

  function mostrarAtivoFocado(evento) {
    const no = evento.target.closest(".mapa-no");
    if (no === null) {
      return;
    }
    const posicao = no.transform.baseVal.consolidate().matrix;
    const estaVisivel =
      posicao.e > camera.x + FOLGA_PARA_MOSTRAR_O_ATIVO_FOCADO &&
      posicao.e < camera.x + visivel.largura - FOLGA_PARA_MOSTRAR_O_ATIVO_FOCADO &&
      posicao.f > camera.y + FOLGA_PARA_MOSTRAR_O_ATIVO_FOCADO &&
      posicao.f < camera.y + visivel.altura - FOLGA_PARA_MOSTRAR_O_ATIVO_FOCADO;
    if (!estaVisivel) {
      moverCameraPara(posicao.e - visivel.largura / 2, posicao.f - visivel.altura / 2);
      mostrarCamera();
    }
  }

  moverCameraPara(camera.x, camera.y);
  mostrarCamera();
  desenho.setAttribute("width", String(visivel.largura));
  desenho.setAttribute("height", String(visivel.altura));
  desenho.classList.add(
    medidas.ehCelular ? "mapa-arrastavel-na-horizontal" : "mapa-arrastavel",
  );
  desenho.addEventListener("pointerdown", comecar);
  desenho.addEventListener("pointermove", mover);
  desenho.addEventListener("pointerup", terminar);
  desenho.addEventListener("pointercancel", terminar);
  desenho.addEventListener("click", impedirCliqueDepoisDeArrastar, true);
  desenho.addEventListener("focusin", mostrarAtivoFocado);
}

export function centralizarCamera(medidas) {
  return {
    x: (medidas.desenho.largura - medidas.visivel.largura) / 2,
    y: (medidas.desenho.altura - medidas.visivel.altura) / 2,
  };
}

function limitar(valor, minimo, maximo) {
  return Math.min(Math.max(valor, minimo), maximo);
}
