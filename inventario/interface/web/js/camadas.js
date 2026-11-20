const pilhaDeCamadas = [];

export function iniciarCamadas() {
  document.addEventListener("keydown", tratarTeclaEsc);
  document.addEventListener("pointerdown", tratarToqueFora);
}

export function abrirCamada(camada) {
  camada.focoAnterior = document.activeElement;
  pilhaDeCamadas.push(camada);
  atualizarBloqueioDaPagina();
}

export function fecharCamada(camada) {
  const posicao = pilhaDeCamadas.indexOf(camada);
  if (posicao === -1) {
    return;
  }
  pilhaDeCamadas.splice(posicao, 1);
  atualizarBloqueioDaPagina();
}

export function devolverFoco(camada) {
  const focoAnterior = camada.focoAnterior;
  if (focoAnterior && focoAnterior.isConnected && !focoAnterior.closest("[inert]")) {
    focoAnterior.focus({ preventScroll: true });
  }
}

function camadaDoTopo() {
  return pilhaDeCamadas[pilhaDeCamadas.length - 1];
}

function atualizarBloqueioDaPagina() {
  let algumaCamadaBloqueiaAPagina = false;
  for (const camada of pilhaDeCamadas) {
    if (camada.bloqueiaAPagina) {
      algumaCamadaBloqueiaAPagina = true;
    }
  }
  document.getElementById("aplicacao").inert = algumaCamadaBloqueiaAPagina;
  document.documentElement.classList.toggle("pagina-bloqueada", algumaCamadaBloqueiaAPagina);
}

function tratarTeclaEsc(evento) {
  const topo = camadaDoTopo();
  if (evento.key !== "Escape" || topo === undefined) {
    return;
  }
  evento.preventDefault();
  topo.pedirFechamento();
}

function tratarToqueFora(evento) {
  const topo = camadaDoTopo();
  if (topo === undefined) {
    return;
  }
  for (const area of topo.areasDeDentro) {
    if (area.contains(evento.target)) {
      return;
    }
  }
  topo.pedirFechamento();
}
