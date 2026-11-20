import { iniciarCamadas } from "./camadas.js";
import { carregarIcones } from "./icones.js";
import { marcarTelaAtiva, montarNavegacao } from "./navegacao.js";
import { iniciarRoteador } from "./roteador.js";
import { ROTA_NAO_ENCONTRADA, ROTAS } from "./rotas.js";

async function iniciarAplicacao() {
  await carregarIcones();
  iniciarCamadas();
  montarNavegacao();
  iniciarRoteador({
    rotas: ROTAS,
    rotaNaoEncontrada: ROTA_NAO_ENCONTRADA,
    aoTrocarDeTela: marcarTelaAtiva,
  });
}

iniciarAplicacao();
