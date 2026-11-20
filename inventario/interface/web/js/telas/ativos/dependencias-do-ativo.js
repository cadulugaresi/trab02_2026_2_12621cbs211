import { cadastrarDependencia, listarAtivos, removerDependencia } from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { criarBotao, liberarBotao, marcarBotaoComoOcupado } from "../../componentes/botoes.js";
import { criarLinhaDeCampo, mostrarAjuda } from "../../componentes/campos.js";
import { criarControleDeslizante } from "../../componentes/controle-deslizante.js";
import { criarMenuComBusca } from "../../componentes/menu-com-busca.js";
import { criarElemento } from "../../elementos.js";
import { formatarFracao } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { iconeDoTipo, indexarAtivosPorId } from "./apresentacao-do-ativo.js";
import { criarMiniMapa } from "./mini-mapa.js";

const MENOR_FRACAO = 0.01;
const FRACAO_SUGERIDA = 0.3;

export function criarSecaoDeDependencias({ idAtivo, ativosPorId, aoMudar, mostrarFalha }) {
  const conteudo = criarElemento("div", { classe: "conteudo-das-dependencias" });
  const secao = criarElemento("section", { classe: "secao-da-janela" }, [
    criarElemento("h3", { classe: "titulo-de-secao secao-da-janela-titulo", texto: "Dependências" }),
    conteudo,
  ]);

  async function recarregar() {
    const ativos = await listarAtivos();
    mostrar(indexarAtivosPorId(ativos));
    aoMudar();
  }

  function mostrar(ativosAtuais) {
    const ativo = ativosAtuais.get(idAtivo);
    const dependeDe = listarDependeDe(ativo, ativosAtuais);
    const dependemDele = listarDependemDele(ativo, ativosAtuais);
    const acoes = { recarregar, mostrarFalha };

    conteudo.replaceChildren();
    if (dependeDe.length > 0 || dependemDele.length > 0) {
      conteudo.append(criarMiniMapa({ ativoCentral: ativo, dependeDe, dependemDele }));
    }
    conteudo.append(
      criarElemento("div", { classe: "colunas-de-dependencias" }, [
        criarColuna("Dependem dele", dependemDele, "Nenhum ativo depende dele.", null, acoes),
        criarColuna("Depende de", dependeDe, "Não depende de nenhum ativo.", ativo, acoes),
      ]),
      criarAreaDeAdicionar(ativo, ativosAtuais, acoes),
    );
  }

  mostrar(ativosPorId);
  return secao;
}

function listarDependeDe(ativo, ativosPorId) {
  const vizinhos = [];
  for (const dependencia of ativo.dependencias) {
    const ativoDoQualDepende = ativosPorId.get(dependencia.id_ativo_do_qual_depende);
    if (ativoDoQualDepende) {
      vizinhos.push({ ativo: ativoDoQualDepende, fracao: dependencia.fracao });
    }
  }
  return vizinhos;
}

function listarDependemDele(ativo, ativosPorId) {
  const vizinhos = [];
  for (const outroAtivo of ativosPorId.values()) {
    for (const dependencia of outroAtivo.dependencias) {
      if (dependencia.id_ativo_do_qual_depende === ativo.id) {
        vizinhos.push({ ativo: outroAtivo, fracao: dependencia.fracao });
      }
    }
  }
  return vizinhos;
}

function criarColuna(titulo, vizinhos, textoQuandoVazia, ativoQuePodeRemover, acoes) {
  const lista = criarElemento("ul", { classe: "lista-de-dependencias" });
  for (const vizinho of vizinhos) {
    lista.append(criarItemDeDependencia(vizinho, ativoQuePodeRemover, acoes));
  }
  if (vizinhos.length === 0) {
    lista.append(criarElemento("li", { classe: "texto-de-apoio", texto: textoQuandoVazia }));
  }
  return criarElemento("div", { classe: "coluna-de-dependencias" }, [
    criarElemento("p", { classe: "legenda", texto: titulo }),
    lista,
  ]);
}

function criarItemDeDependencia(vizinho, ativoQuePodeRemover, acoes) {
  const item = criarElemento("li", { classe: "item-de-dependencia" }, [
    criarElemento("a", { classe: "item-de-dependencia-nome", href: `#/ativos/${vizinho.ativo.id}` }, [
      criarIcone(iconeDoTipo(vizinho.ativo.tipo)),
      criarElemento("span", { texto: vizinho.ativo.nome }),
    ]),
    criarElemento("span", {
      classe: "item-de-dependencia-fracao",
      texto: `fração ${formatarFracao(vizinho.fracao)}`,
    }),
  ]);
  if (ativoQuePodeRemover !== null) {
    item.append(criarBotaoDeRemover(ativoQuePodeRemover, vizinho.ativo, acoes));
  }
  return item;
}

function criarBotaoDeRemover(ativo, ativoDoQualDepende, acoes) {
  const botao = criarBotao({
    variacao: "icone",
    icone: "fechar",
    rotuloAcessivel: `Remover a dependência de ${ativoDoQualDepende.nome}`,
  });
  botao.addEventListener("click", async () => {
    botao.disabled = true;
    try {
      await removerDependencia(ativo.id, ativoDoQualDepende.id);
      mostrarAvisoDeSucesso("Dependência removida");
      await acoes.recarregar();
    } catch (erro) {
      botao.disabled = false;
      acoes.mostrarFalha(erro);
    }
  });
  return botao;
}

function criarAreaDeAdicionar(ativo, ativosPorId, acoes) {
  const area = criarElemento("div", { classe: "area-de-nova-dependencia" });
  const botaoDeAbrir = criarBotao({
    texto: "Adicionar dependência",
    variacao: "secundario",
    icone: "mais",
    pequeno: true,
  });
  botaoDeAbrir.addEventListener("click", () => {
    area.replaceChildren(
      criarLinhaDeNovaDependencia(ativo, ativosPorId, acoes, () => {
        area.replaceChildren(botaoDeAbrir);
        botaoDeAbrir.focus();
      }),
    );
  });
  area.append(botaoDeAbrir);
  return area;
}

function criarLinhaDeNovaDependencia(ativo, ativosPorId, acoes, fechar) {
  const fracaoRestante = calcularFracaoRestante(ativo);
  const candidatos = listarCandidatos(ativo, ativosPorId);
  const botaoDeCancelar = criarBotao({
    texto: "Cancelar",
    variacao: "secundario",
    pequeno: true,
    aoClicar: fechar,
  });

  if (fracaoRestante <= MENOR_FRACAO || candidatos.length === 0) {
    const motivo =
      candidatos.length === 0
        ? "Não há outro ativo para escolher."
        : "A soma das frações já chegou ao limite. Remova uma dependência para adicionar outra.";
    return criarElemento("div", { classe: "linha-de-nova-dependencia" }, [
      criarElemento("p", { classe: "texto-de-apoio", texto: motivo }),
      criarElemento("div", { classe: "linha-de-nova-dependencia-botoes" }, [botaoDeCancelar]),
    ]);
  }

  const maiorFracao = arredondarFracao(fracaoRestante - MENOR_FRACAO);
  const menu = criarMenuComBusca({
    rotulo: "Ativo do qual depende",
    itens: candidatos,
    textoQuandoVazio: "Escolha o ativo",
    textoSemResultado: "Nenhum ativo com esse nome ou ID",
  });
  const fracao = criarControleDeslizante({
    minimo: MENOR_FRACAO,
    maximo: maiorFracao,
    passo: MENOR_FRACAO,
    valor: Math.min(FRACAO_SUGERIDA, maiorFracao),
    formatar: formatarFracao,
  });
  const linhaDoAtivo = criarLinhaDeCampo({ rotulo: "Depende de", controle: menu.elemento });
  menu.elemento.addEventListener("change", () => {
    menu.elemento.removeAttribute("aria-invalid");
    mostrarAjuda(linhaDoAtivo.textoDeAjuda, "");
  });
  const linhaDaFracao = criarLinhaDeCampo({
    rotulo: "Fração",
    controle: fracao.elemento,
    alvoDoRotulo: fracao.campo,
    ajuda: `A fração precisa ser menor que ${formatarFracao(fracaoRestante)}`,
    explicacaoDoConceito:
      "A fração diz quanto do risco do outro ativo passa para este. " +
      "A soma das frações de um ativo precisa ficar abaixo de 1.",
  });
  const botaoDeAdicionar = criarBotao({ texto: "Adicionar", pequeno: true });

  botaoDeAdicionar.addEventListener("click", async () => {
    const idEscolhido = menu.obterValor();
    if (idEscolhido === null) {
      menu.elemento.setAttribute("aria-invalid", "true");
      mostrarAjuda(linhaDoAtivo.textoDeAjuda, "Escolha o ativo do qual este depende", true);
      menu.elemento.focus();
      return;
    }
    marcarBotaoComoOcupado(botaoDeAdicionar, "Adicionando…");
    try {
      await cadastrarDependencia(ativo.id, idEscolhido, fracao.obterValor());
      mostrarAvisoDeSucesso("Dependência adicionada");
      await acoes.recarregar();
    } catch (erro) {
      liberarBotao(botaoDeAdicionar);
      acoes.mostrarFalha(erro);
    }
  });

  return criarElemento("div", { classe: "linha-de-nova-dependencia" }, [
    linhaDoAtivo.elemento,
    linhaDaFracao.elemento,
    criarElemento("div", { classe: "linha-de-nova-dependencia-botoes" }, [
      botaoDeCancelar,
      botaoDeAdicionar,
    ]),
  ]);
}

function calcularFracaoRestante(ativo) {
  let somaDasFracoes = 0;
  for (const dependencia of ativo.dependencias) {
    somaDasFracoes += dependencia.fracao;
  }
  return arredondarFracao(1 - somaDasFracoes);
}

function listarCandidatos(ativo, ativosPorId) {
  const idsQueJaSaoDependencias = new Set();
  for (const dependencia of ativo.dependencias) {
    idsQueJaSaoDependencias.add(dependencia.id_ativo_do_qual_depende);
  }
  const candidatos = [];
  for (const outroAtivo of ativosPorId.values()) {
    if (outroAtivo.id !== ativo.id && !idsQueJaSaoDependencias.has(outroAtivo.id)) {
      candidatos.push({ valor: outroAtivo.id, rotulo: outroAtivo.nome });
    }
  }
  return candidatos;
}

function arredondarFracao(fracao) {
  return Math.round(fracao * 100) / 100;
}
