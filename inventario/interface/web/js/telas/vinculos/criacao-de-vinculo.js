import { vincularVulnerabilidade } from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { criarBotao, liberarBotao, marcarBotaoComoOcupado } from "../../componentes/botoes.js";
import { criarLinhaComValidacao } from "../../componentes/campos.js";
import { criarMenuComBusca } from "../../componentes/menu-com-busca.js";
import { criarMenuSuspenso } from "../../componentes/menu-suspenso.js";
import { criarElemento } from "../../elementos.js";
import { encontrarValorPeloNome } from "../../opcoes.js";
import { navegarPara } from "../../roteador.js";
import { validarEscolha } from "../../validacoes.js";

const MENSAGEM_DE_VINCULO_REPETIDO = "Esta vulnerabilidade já está vinculada a este ativo.";

export function criarCriacaoDeVinculo({ opcoes, idAtivoInicial, aoVincular, aoFalhar }) {
  const ativo = criarMenuComBusca({
    rotulo: "Ativo",
    textoQuandoVazio: "Escolha o ativo",
    textoSemResultado: "Nenhum ativo com esse nome ou ID",
  });
  const vulnerabilidade = criarMenuComBusca({
    rotulo: "Vulnerabilidade",
    textoQuandoVazio: "Escolha a vulnerabilidade",
    textoSemResultado: "Nenhuma vulnerabilidade com esse nome ou ID",
  });
  const status = criarMenuSuspenso({
    rotulo: "Status",
    opcoes: opcoes.statusDeTratamento,
    valor: encontrarValorPeloNome(opcoes.statusDeTratamento, "ABERTA"),
  });
  const linhas = {
    ativo: criarLinhaComValidacao({ rotulo: "Ativo", controle: ativo.elemento }),
    vulnerabilidade: criarLinhaComValidacao({
      rotulo: "Vulnerabilidade",
      controle: vulnerabilidade.elemento,
    }),
    status: criarLinhaComValidacao({ rotulo: "Status", controle: status.elemento }),
  };
  const botaoDeVincular = criarBotao({ texto: "Vincular" });
  const formulario = criarElemento("form", { classe: "criacao-de-vinculo", novalidate: true }, [
    linhas.ativo.elemento,
    linhas.vulnerabilidade.elemento,
    linhas.status.elemento,
    criarElemento("div", { classe: "criacao-de-vinculo-botao" }, [botaoDeVincular]),
  ]);
  botaoDeVincular.type = "submit";

  const aviso = criarElemento("div", { classe: "criacao-de-vinculo-aviso", hidden: true });
  const elemento = criarElemento("section", { "aria-label": "Novo vínculo" }, [formulario, aviso]);
  let ativosAtuais = [];
  let idAtivoParaEscolher = idAtivoInicial;

  function atualizarItens(ativos, vulnerabilidades) {
    ativosAtuais = ativos;
    const faltaAlgo = ativos.length === 0 || vulnerabilidades.length === 0;
    formulario.hidden = faltaAlgo;
    aviso.hidden = !faltaAlgo;
    if (faltaAlgo) {
      mostrarAvisoDoQueFalta(aviso, ativos.length === 0, vulnerabilidades.length === 0);
      return;
    }
    ativo.definirItens(montarItensDeAtivos(ativos));
    vulnerabilidade.definirItens(montarItensDeVulnerabilidades(vulnerabilidades));
    if (idAtivoParaEscolher !== null && existeAtivo(idAtivoParaEscolher)) {
      ativo.definirValor(idAtivoParaEscolher);
    }
    idAtivoParaEscolher = null;
  }

  function existeAtivo(idAtivo) {
    for (const ativoAtual of ativosAtuais) {
      if (ativoAtual.id === idAtivo) {
        return true;
      }
    }
    return false;
  }

  function validar() {
    const erros = [];
    validarEscolha(erros, "ativo", ativo.obterValor());
    validarEscolha(erros, "vulnerabilidade", vulnerabilidade.obterValor());
    if (erros.length === 0 && jaEstaVinculada(ativo.obterValor(), vulnerabilidade.obterValor())) {
      erros.push({ campo: "vulnerabilidade", mensagem: MENSAGEM_DE_VINCULO_REPETIDO });
    }
    return erros;
  }

  function jaEstaVinculada(idAtivo, idVulnerabilidade) {
    for (const ativoAtual of ativosAtuais) {
      if (ativoAtual.id === idAtivo) {
        return ativoTemAVulnerabilidade(ativoAtual, idVulnerabilidade);
      }
    }
    return false;
  }

  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    for (const linha of Object.values(linhas)) {
      linha.limparErro();
    }
    const erros = validar();
    if (erros.length > 0) {
      for (const erro of erros) {
        linhas[erro.campo].mostrarErro(erro.mensagem);
      }
      linhas[erros[0].campo].alvo.focus();
      return;
    }

    marcarBotaoComoOcupado(botaoDeVincular, "Vinculando…");
    try {
      await vincularVulnerabilidade(ativo.obterValor(), vulnerabilidade.obterValor(), status.obterValor());
      mostrarAvisoDeSucesso("Vulnerabilidade vinculada");
      vulnerabilidade.definirValor(null);
      await aoVincular();
    } catch (erro) {
      aoFalhar(erro);
    } finally {
      liberarBotao(botaoDeVincular);
    }
  });

  return { elemento, atualizarItens };
}

function ativoTemAVulnerabilidade(ativo, idVulnerabilidade) {
  for (const vinculo of ativo.vulnerabilidades) {
    if (vinculo.id_vulnerabilidade === idVulnerabilidade) {
      return true;
    }
  }
  return false;
}

function montarItensDeAtivos(ativos) {
  const itens = [];
  for (const ativo of ativos) {
    itens.push({ valor: ativo.id, rotulo: ativo.nome });
  }
  return itens;
}

function montarItensDeVulnerabilidades(vulnerabilidades) {
  const itens = [];
  for (const vulnerabilidade of vulnerabilidades) {
    itens.push({
      valor: vulnerabilidade.id_vulnerabilidade,
      rotulo: vulnerabilidade.nome_vulnerabilidade,
    });
  }
  return itens;
}

function mostrarAvisoDoQueFalta(aviso, faltaAtivo, faltaVulnerabilidade) {
  const botoes = [];
  if (faltaAtivo) {
    botoes.push(
      criarBotao({
        texto: "Novo ativo",
        variacao: "secundario",
        icone: "mais",
        aoClicar: () => navegarPara("/ativos/novo"),
      }),
    );
  }
  if (faltaVulnerabilidade) {
    botoes.push(
      criarBotao({
        texto: "Nova vulnerabilidade",
        variacao: "secundario",
        icone: "mais",
        aoClicar: () => navegarPara("/vulnerabilidades/novo"),
      }),
    );
  }
  aviso.replaceChildren(
    criarElemento("p", {
      classe: "texto-de-apoio",
      texto: "Para vincular, cadastre pelo menos um ativo e uma vulnerabilidade.",
    }),
    criarElemento("div", { classe: "criacao-de-vinculo-aviso-botoes" }, botoes),
  );
}
