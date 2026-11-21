import { esconderComTransicao, mostrarComTransicao } from "./animacoes.js";
import { abrirCamada, devolverFoco, fecharCamada } from "./camadas.js";
import { criarBotao } from "./componentes/botoes.js";
import { abrirFlutuante } from "./componentes/flutuante.js";
import { criarElemento, gerarIdentificador } from "./elementos.js";
import { criarIcone } from "./icones.js";

const TELAS_DA_NAVEGACAO = [
  { nome: "Início", caminho: "/", icone: "inicio" },
  {
    nome: "Ativos",
    caminho: "/ativos",
    icone: "ativos",
    subopcoes: [
      { nome: "Lista de ativos", caminho: "/ativos", incluiDetalhes: true },
      { nome: "Cadastrar ativo", caminho: "/ativos/novo" },
      { nome: "Mapa de grafos", caminho: "/ativos/mapa" },
    ],
  },
  {
    nome: "Vulnerabilidades",
    caminho: "/vulnerabilidades",
    icone: "vulnerabilidades",
    subopcoes: [
      { nome: "Lista de vulnerabilidades", caminho: "/vulnerabilidades", incluiDetalhes: true },
      { nome: "Cadastrar vulnerabilidade", caminho: "/vulnerabilidades/novo" },
    ],
  },
  { nome: "Vínculos", caminho: "/vinculos", icone: "vinculos" },
  { nome: "Ranking de riscos", caminho: "/ranking", icone: "ranking" },
];

const OPCOES_DO_CADASTRAR = [
  { nome: "Novo ativo", caminho: "/ativos/novo", icone: "ativos" },
  { nome: "Nova vulnerabilidade", caminho: "/vulnerabilidades/novo", icone: "vulnerabilidades" },
];

const linksDasTelas = [];
let painelAberto = null;
let caminhoDaTelaAtual = "/";

export function montarNavegacao() {
  montarFaixaDeIcones();
  montarAreaInferior();
}

export function marcarTelaAtiva(caminho, rota) {
  caminhoDaTelaAtual = caminho;
  for (const link of linksDasTelas) {
    marcarLink(link, caminho);
  }
  document
    .getElementById("area-inferior")
    .toggleAttribute("data-sem-cadastrar", rota.escondeCadastrar === true);
}

function marcarLink(link, caminho) {
  if (pertenceATela(caminho, link.dataset.caminho)) {
    link.setAttribute("aria-current", "page");
  } else {
    link.removeAttribute("aria-current");
  }
}

function ehASubopcaoAtual(caminho, subopcao) {
  if (caminho === subopcao.caminho) {
    return true;
  }
  if (!subopcao.incluiDetalhes || !caminho.startsWith(`${subopcao.caminho}/`)) {
    return false;
  }
  const resto = caminho.slice(subopcao.caminho.length + 1);
  return /^\d+$/.test(resto);
}

function pertenceATela(caminho, caminhoDaTela) {
  if (caminhoDaTela === "/") {
    return caminho === "/";
  }
  return caminho === caminhoDaTela || caminho.startsWith(`${caminhoDaTela}/`);
}

function montarFaixaDeIcones() {
  const faixa = document.getElementById("faixa-de-navegacao");
  const botaoDoPainel = criarBotao({
    variacao: "icone",
    icone: "abrirPainel",
    rotuloAcessivel: "Abrir o menu",
    aoClicar: (evento) => alternarPainel(evento.currentTarget),
  });
  botaoDoPainel.classList.add("faixa-botao-do-painel");
  botaoDoPainel.setAttribute("aria-expanded", "false");

  const lista = criarElemento("ul", { classe: "faixa-lista" });
  for (const tela of TELAS_DA_NAVEGACAO) {
    const link = criarElemento(
      "a",
      { classe: "faixa-item", href: `#${tela.caminho}`, "data-caminho": tela.caminho },
      [
        criarIcone(tela.icone),
        criarElemento("span", { classe: "faixa-rotulo", texto: tela.nome }),
      ],
    );
    linksDasTelas.push(link);
    lista.append(criarElemento("li", {}, [link]));
  }
  faixa.append(botaoDoPainel, lista);
}

function montarAreaInferior() {
  const area = document.getElementById("area-inferior");
  const botaoDoMenu = criarBotao({ texto: "Menu", icone: "menu" });
  botaoDoMenu.classList.add("botao-do-menu");
  botaoDoMenu.setAttribute("aria-expanded", "false");
  botaoDoMenu.addEventListener("click", () => alternarPainel(botaoDoMenu));
  area.append(criarBotaoCadastrar(), botaoDoMenu);
}

function criarBotaoCadastrar() {
  const botao = criarElemento(
    "button",
    {
      type: "button",
      classe: "botao botao-principal botao-cadastrar",
      "aria-haspopup": "true",
      "aria-expanded": "false",
    },
    [
      criarElemento("span", { classe: "circulo-do-mais" }, [criarIcone("mais")]),
      criarElemento("span", { texto: "Cadastrar" }),
    ],
  );
  let menuAberto = null;
  botao.addEventListener("click", () => {
    if (botao.getAttribute("aria-expanded") === "true") {
      menuAberto.fechar();
      return;
    }
    menuAberto = abrirMenuDoCadastrar(botao);
  });
  return botao;
}

function abrirMenuDoCadastrar(ancora) {
  const lista = criarElemento("ul", { classe: "menu-do-cadastrar", "aria-label": "Cadastrar" });
  const links = [];
  for (const opcao of OPCOES_DO_CADASTRAR) {
    const link = criarElemento(
      "a",
      { classe: "menu-do-cadastrar-item", href: `#${opcao.caminho}` },
      [criarIcone(opcao.icone), criarElemento("span", { texto: opcao.nome })],
    );
    links.push(link);
    lista.append(criarElemento("li", {}, [link]));
  }

  const ladoPreferido = ancora.closest(".painel") ? "abaixo" : "acima";
  const menu = abrirFlutuante({
    conteudo: lista,
    ancora: ancora,
    preferencias: { lado: ladoPreferido, alinhamento: "centro" },
  });
  for (const link of links) {
    link.addEventListener("click", () => {
      menu.fechar();
      fecharPainel();
    });
  }
  lista.addEventListener("keydown", (evento) => moverFocoEntreLinks(evento, links));
  links[0].focus({ preventScroll: true });
  return menu;
}

function moverFocoEntreLinks(evento, links) {
  const posicaoAtual = links.indexOf(document.activeElement);
  if (evento.key === "ArrowDown") {
    evento.preventDefault();
    links[Math.min(posicaoAtual + 1, links.length - 1)].focus();
  } else if (evento.key === "ArrowUp") {
    evento.preventDefault();
    links[Math.max(posicaoAtual - 1, 0)].focus();
  }
}

function alternarPainel(ancora) {
  if (painelAberto !== null) {
    fecharPainel();
    return;
  }
  abrirPainel(ancora);
}

function abrirPainel(ancora) {
  const painel = criarElemento("nav", { classe: "painel", "aria-label": "Menu" }, [
    criarTopoDoPainel(),
    criarElemento("div", { classe: "painel-cadastrar" }, [criarBotaoCadastrar()]),
    criarListaDoPainel(),
  ]);
  const camadaDoPainel = criarElemento("div", { classe: "painel-camada" }, [
    criarElemento("div", { classe: "veu" }),
    painel,
  ]);
  const camada = {
    areasDeDentro: [painel],
    bloqueiaAPagina: true,
    pedirFechamento: fecharPainel,
  };

  document.body.append(camadaDoPainel);
  apontarOrigemPara(painel, ancora);
  abrirCamada(camada);
  ancora.setAttribute("aria-expanded", "true");
  mostrarComTransicao(camadaDoPainel);
  painelAberto = { camadaDoPainel, painel, camada, ancora };
  painel.querySelector(".painel-item").focus({ preventScroll: true });
}

async function fecharPainel() {
  if (painelAberto === null) {
    return;
  }
  const { camadaDoPainel, painel, camada, ancora } = painelAberto;
  painelAberto = null;
  fecharCamada(camada);
  ancora.setAttribute("aria-expanded", "false");
  devolverFoco(camada);
  await esconderComTransicao(camadaDoPainel, painel);
  camadaDoPainel.remove();
}

function criarTopoDoPainel() {
  const botaoDeFechar = criarBotao({
    variacao: "icone",
    icone: "fechar",
    rotuloAcessivel: "Fechar o menu",
    aoClicar: fecharPainel,
  });
  return criarElemento("div", { classe: "painel-topo" }, [
    criarElemento("p", { classe: "painel-titulo", texto: "Inventário" }),
    botaoDeFechar,
  ]);
}

function criarListaDoPainel() {
  const lista = criarElemento("ul", { classe: "painel-lista" });
  const grupos = [];
  for (const tela of TELAS_DA_NAVEGACAO) {
    if (tela.subopcoes === undefined) {
      lista.append(criarElemento("li", {}, [criarLinkDoPainel(tela)]));
      continue;
    }
    const grupo = criarGrupoDoPainel(tela);
    grupo.botao.addEventListener("click", () => {
      const vaiAbrir = !grupo.estaAberto();
      for (const outroGrupo of grupos) {
        outroGrupo.definirAberto(false);
      }
      grupo.definirAberto(vaiAbrir);
    });
    grupos.push(grupo);
    lista.append(grupo.elemento);
  }
  return lista;
}

function criarLinkDoPainel(tela) {
  const link = criarElemento(
    "a",
    { classe: "painel-item", href: `#${tela.caminho}`, "data-caminho": tela.caminho },
    [criarIcone(tela.icone), criarElemento("span", { texto: tela.nome })],
  );
  marcarLink(link, caminhoDaTelaAtual);
  link.addEventListener("click", fecharPainel);
  return link;
}

function criarGrupoDoPainel(tela) {
  const identificadorDasSubopcoes = gerarIdentificador("subopcoes");
  const botao = criarElemento(
    "button",
    {
      type: "button",
      classe: "painel-item painel-grupo",
      "aria-expanded": "false",
      "aria-controls": identificadorDasSubopcoes,
    },
    [
      criarIcone(tela.icone),
      criarElemento("span", { texto: tela.nome }),
      criarIcone("setaParaBaixo", "painel-grupo-seta"),
    ],
  );
  botao.toggleAttribute("data-tela-atual", pertenceATela(caminhoDaTelaAtual, tela.caminho));

  const listaDeSubopcoes = criarElemento("ul", { classe: "painel-subopcoes-lista" });
  for (const subopcao of tela.subopcoes) {
    const link = criarElemento("a", {
      classe: "painel-subopcao",
      href: `#${subopcao.caminho}`,
      texto: subopcao.nome,
    });
    if (ehASubopcaoAtual(caminhoDaTelaAtual, subopcao)) {
      link.setAttribute("aria-current", "page");
    }
    link.addEventListener("click", fecharPainel);
    listaDeSubopcoes.append(criarElemento("li", {}, [link]));
  }
  const subopcoes = criarElemento(
    "div",
    { classe: "painel-subopcoes", id: identificadorDasSubopcoes },
    [listaDeSubopcoes],
  );
  subopcoes.inert = true;

  return {
    elemento: criarElemento("li", {}, [botao, subopcoes]),
    botao: botao,
    estaAberto: () => botao.getAttribute("aria-expanded") === "true",
    definirAberto: (aberto) => {
      botao.setAttribute("aria-expanded", aberto ? "true" : "false");
      subopcoes.inert = !aberto;
    },
  };
}

function apontarOrigemPara(painel, ancora) {
  const caixaDaAncora = ancora.getBoundingClientRect();
  const origemHorizontal = caixaDaAncora.left + caixaDaAncora.width / 2 - painel.offsetLeft;
  const origemVertical = caixaDaAncora.top + caixaDaAncora.height / 2 - painel.offsetTop;
  painel.style.transformOrigin = `${origemHorizontal}px ${origemVertical}px`;
}
