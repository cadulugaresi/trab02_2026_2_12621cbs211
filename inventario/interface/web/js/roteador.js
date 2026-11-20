import { fecharJanela } from "./componentes/janela.js";
import { criarElemento } from "./elementos.js";

let rotasConhecidas = [];
let rotaDesconhecida = null;
let avisarTrocaDeTela = () => {};
let telaMontada = null;
let enderecosDaJanela = [];
let janelaAbriuSobreUmaTela = false;
let ehAPrimeiraNavegacao = true;
let navegacoesDentroDoSistema = 0;

export function iniciarRoteador({ rotas, rotaNaoEncontrada, aoTrocarDeTela }) {
  rotasConhecidas = rotas;
  rotaDesconhecida = rotaNaoEncontrada;
  avisarTrocaDeTela = aoTrocarDeTela;
  window.addEventListener("hashchange", tratarMudancaDeEndereco);
  tratarMudancaDeEndereco();
}

export function navegarPara(endereco) {
  location.hash = `#${endereco}`;
}

export function trocarEnderecoPor(endereco) {
  location.replace(`#${endereco}`);
}

export function voltarOuIrPara(endereco) {
  if (navegacoesDentroDoSistema > 0) {
    history.back();
    return;
  }
  trocarEnderecoPor(endereco);
}

export function atualizarTelaAtual() {
  if (telaMontada !== null && telaMontada.atualizar) {
    telaMontada.atualizar();
  }
}

function tratarMudancaDeEndereco() {
  const endereco = lerEnderecoAtual();
  const { caminho, busca } = separarEndereco(endereco);
  const { rota, parametros } = encontrarRota(caminho);

  if (rota.janela) {
    mostrarRotaDeJanela(endereco, rota, parametros);
  } else {
    sairDaJanela();
    mostrarTela(endereco, rota, parametros, busca);
  }
  if (!ehAPrimeiraNavegacao) {
    navegacoesDentroDoSistema += 1;
  }
  ehAPrimeiraNavegacao = false;
}

function lerEnderecoAtual() {
  const endereco = location.hash.slice(1);
  if (endereco === "" || endereco === "/") {
    return "/";
  }
  return endereco;
}

function separarEndereco(endereco) {
  const posicaoDaBusca = endereco.indexOf("?");
  if (posicaoDaBusca === -1) {
    return { caminho: endereco, busca: new URLSearchParams() };
  }
  return {
    caminho: endereco.slice(0, posicaoDaBusca),
    busca: new URLSearchParams(endereco.slice(posicaoDaBusca + 1)),
  };
}

function encontrarRota(caminho) {
  for (const rota of rotasConhecidas) {
    const parametros = compararComOModelo(rota.caminho, caminho);
    if (parametros !== null) {
      return { rota, parametros };
    }
  }
  return { rota: rotaDesconhecida, parametros: {} };
}

function compararComOModelo(modelo, caminho) {
  const partesDoModelo = dividirEmPartes(modelo);
  const partesDoCaminho = dividirEmPartes(caminho);
  if (partesDoModelo.length !== partesDoCaminho.length) {
    return null;
  }

  const parametros = {};
  for (const [indice, parteDoModelo] of partesDoModelo.entries()) {
    const parteDoCaminho = partesDoCaminho[indice];
    if (parteDoModelo.startsWith(":")) {
      if (!/^\d+$/.test(parteDoCaminho)) {
        return null;
      }
      parametros[parteDoModelo.slice(1)] = Number(parteDoCaminho);
    } else if (parteDoModelo !== parteDoCaminho) {
      return null;
    }
  }
  return parametros;
}

function dividirEmPartes(caminho) {
  const partes = [];
  for (const parte of caminho.split("/")) {
    if (parte !== "") {
      partes.push(parte);
    }
  }
  return partes;
}

function mostrarTela(endereco, rota, parametros, busca) {
  if (telaMontada !== null && telaMontada.endereco === endereco) {
    return;
  }
  if (telaMontada !== null && telaMontada.desmontar) {
    telaMontada.desmontar();
  }

  const conteudo = document.getElementById("conteudo");
  const tela = criarElemento("div", { classe: "tela" });
  conteudo.replaceChildren(tela);
  const controleDaTela = rota.montar(tela, { parametros, busca }) ?? {};
  telaMontada = {
    endereco: endereco,
    serveDeFundo: rota.serveDeFundo === true,
    desmontar: controleDaTela.desmontar,
    atualizar: controleDaTela.atualizar,
  };

  document.title = `${rota.titulo} · Inventário`;
  avisarTrocaDeTela(separarEndereco(endereco).caminho, rota);
  window.scrollTo(0, 0);
  if (!ehAPrimeiraNavegacao) {
    conteudo.focus({ preventScroll: true });
  }
}

function mostrarRotaDeJanela(endereco, rota, parametros) {
  if (telaMontada === null || !telaMontada.serveDeFundo) {
    const rotaDoFundo = encontrarRota(rota.fundo);
    mostrarTela(rota.fundo, rotaDoFundo.rota, rotaDoFundo.parametros, new URLSearchParams());
    janelaAbriuSobreUmaTela = false;
    enderecosDaJanela = [];
  } else if (enderecosDaJanela.length === 0) {
    janelaAbriuSobreUmaTela = true;
  }

  registrarEnderecoDaJanela(endereco);
  rota.janela(parametros, {
    pedirFechamento: fecharJanelaPeloEndereco,
    voltar: enderecosDaJanela.length > 1 ? () => history.back() : undefined,
    continuaAberta: () => lerEnderecoAtual() === endereco,
  });
}

function registrarEnderecoDaJanela(endereco) {
  const quantidade = enderecosDaJanela.length;
  if (quantidade >= 2 && enderecosDaJanela[quantidade - 2] === endereco) {
    enderecosDaJanela.pop();
  } else if (enderecosDaJanela[quantidade - 1] !== endereco) {
    enderecosDaJanela.push(endereco);
  }
}

function fecharJanelaPeloEndereco() {
  if (janelaAbriuSobreUmaTela) {
    history.go(-enderecosDaJanela.length);
    return;
  }
  location.replace(`#${telaMontada.endereco}`);
}

function sairDaJanela() {
  if (enderecosDaJanela.length === 0) {
    return;
  }
  enderecosDaJanela = [];
  fecharJanela();
}
