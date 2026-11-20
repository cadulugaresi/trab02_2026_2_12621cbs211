import { buscarAtivo, cadastrarAtivo, editarAtivo } from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { liberarBotao, marcarBotaoComoOcupado } from "../../componentes/botoes.js";
import {
  criarCampoDeNumero,
  criarCampoDeTexto,
  criarLinhaComValidacao,
  mostrarAjuda,
} from "../../componentes/campos.js";
import { criarContador } from "../../componentes/contador.js";
import { criarControleDeslizante } from "../../componentes/controle-deslizante.js";
import { criarMenuSuspenso } from "../../componentes/menu-suspenso.js";
import { criarElemento, gerarIdentificador } from "../../elementos.js";
import { formatarNumero } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { carregarOpcoes, encontrarOpcao } from "../../opcoes.js";
import { trocarEnderecoPor } from "../../roteador.js";
import {
  validarEscolha,
  validarInteiroPositivo,
  validarNumeroPositivo,
  validarTextoObrigatorio,
} from "../../validacoes.js";
import {
  criarEstruturaDoFormulario,
  criarGrupoDoFormulario,
  mostrarErrosNasLinhas,
} from "../estrutura-do-formulario.js";
import { rotuloDoTipo } from "./apresentacao-do-ativo.js";

const MENOR_FATOR = 0.1;
const MAIOR_FATOR = 2;
const MENSAGEM_DE_ID_REPETIDO = "Já existe um ativo cadastrado com este ID.";
const CAMPOS_DE_CADA_TIPO = {
  Notebook: ["sistemaOperacional", "tela"],
  Servidor: ["ram", "armazenamento"],
  Roteador: ["portas", "velocidade"],
  Impressora: ["cor", "tecnologia"],
};

export function montarTelaDeNovoAtivo(tela) {
  montarFormularioDeAtivo(tela, null);
}

export function montarTelaDeEditarAtivo(tela, { parametros }) {
  montarFormularioDeAtivo(tela, parametros.id);
}

function montarFormularioDeAtivo(tela, idEmEdicao) {
  const ehEdicao = idEmEdicao !== null;
  const estrutura = criarEstruturaDoFormulario({
    titulo: ehEdicao ? "Editar ativo" : "Novo ativo",
    textoDoBotao: "Salvar ativo",
    enderecoDeVolta: ehEdicao ? `/ativos/${idEmEdicao}` : "/ativos",
  });
  tela.append(estrutura.formulario);

  Promise.all([carregarOpcoes(), ehEdicao ? buscarAtivo(idEmEdicao) : null])
    .then(([opcoes, ativo]) => {
      const campos = criarCampos(opcoes, ativo);
      estrutura.areaDosCampos.append(campos.elemento);
      estrutura.subtitulo.textContent = ehEdicao
        ? `ID ${ativo.id} · ${ativo.nome}`
        : "Escolha o tipo e preencha os dados do ativo";
      estrutura.botaoDeSalvar.disabled = false;
      estrutura.formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        salvar(campos, idEmEdicao, estrutura);
      });
    })
    .catch((erro) => estrutura.faixa.mostrar(erro.message));
}

async function salvar(campos, idEmEdicao, estrutura) {
  estrutura.faixa.esconder();
  campos.limparErros();
  const erros = campos.validar();
  if (erros.length > 0) {
    campos.mostrarErros(erros);
    return;
  }

  marcarBotaoComoOcupado(estrutura.botaoDeSalvar, "Salvando…");
  try {
    const dadosDoAtivo = campos.montarDadosParaAApi();
    const ativoSalvo =
      idEmEdicao === null
        ? await cadastrarAtivo(dadosDoAtivo)
        : await editarAtivo(idEmEdicao, dadosDoAtivo);
    mostrarAvisoDeSucesso(idEmEdicao === null ? "Ativo cadastrado" : "Ativo atualizado");
    trocarEnderecoPor(`/ativos/${ativoSalvo.id}`);
  } catch (erro) {
    liberarBotao(estrutura.botaoDeSalvar);
    estrutura.faixa.mostrar(erro.message);
    if (erro.message === MENSAGEM_DE_ID_REPETIDO) {
      campos.mostrarErros([{ campo: "id", mensagem: "Escolha outro ID" }]);
    }
  }
}

function criarCampos(opcoes, ativo) {
  const ehEdicao = ativo !== null;
  const controles = criarControles(opcoes, ativo);
  const linhas = criarLinhas(controles, ehEdicao);
  const escolhaDeTipo = criarEscolhaDeTipo(opcoes.tipos, ehEdicao ? ativo.tipo : null, escolherTipo);
  const tituloDosDetalhes = criarElemento("h2", { classe: "titulo-de-secao" });
  const grupoDosDetalhes = criarElemento("section", { classe: "grupo-de-ajustes", hidden: true });
  let tipoEscolhido = ehEdicao ? ativo.tipo : null;

  function escolherTipo(novoTipo) {
    const tipoMudou = tipoEscolhido !== null && novoTipo !== tipoEscolhido;
    tipoEscolhido = novoTipo;
    if (!ehEdicao || tipoMudou) {
      const tipo = encontrarOpcao(opcoes.tipos, novoTipo);
      controles.fator.definirValor(tipo.fatorDeExposicaoPadrao);
    }
    mostrarAjudaDoFator();
    mostrarCamposDoTipo();
    mostrarAjuda(escolhaDeTipo.textoDeAjuda, "");
  }

  function mostrarAjudaDoFator() {
    const tipo = encontrarOpcao(opcoes.tipos, tipoEscolhido);
    const mensagem = tipo
      ? `Padrão do ${tipo.rotulo}: ${formatarNumero(tipo.fatorDeExposicaoPadrao)}`
      : "Escolha o tipo para começar no padrão dele";
    mostrarAjuda(linhas.fator.textoDeAjuda, mensagem);
  }

  function mostrarCamposDoTipo() {
    grupoDosDetalhes.hidden = tipoEscolhido === null;
    if (tipoEscolhido === null) {
      return;
    }
    tituloDosDetalhes.textContent = `Detalhes do ${rotuloDoTipo(tipoEscolhido)}`;
    grupoDosDetalhes.replaceChildren(tituloDosDetalhes);
    for (const nomeDoCampo of CAMPOS_DE_CADA_TIPO[tipoEscolhido]) {
      grupoDosDetalhes.append(linhas[nomeDoCampo].elemento);
    }
  }

  const linhasDeIdentificacao = ehEdicao
    ? [linhas.nome.elemento, linhas.responsavel.elemento]
    : [linhas.id.elemento, linhas.nome.elemento, linhas.responsavel.elemento];

  const elemento = criarElemento("div", {}, [
    criarGrupoDoFormulario("Tipo", [escolhaDeTipo.elemento, escolhaDeTipo.textoDeAjuda]),
    criarGrupoDoFormulario("Identificação", linhasDeIdentificacao),
    criarGrupoDoFormulario("Situação", [linhas.setor.elemento, linhas.status.elemento]),
    criarGrupoDoFormulario("Exposição", [linhas.fator.elemento]),
    grupoDosDetalhes,
  ]);

  mostrarAjudaDoFator();
  mostrarCamposDoTipo();

  function validar() {
    const erros = [];
    if (tipoEscolhido === null) {
      erros.push({ campo: "tipo", mensagem: "Escolha o tipo do ativo" });
    }
    if (!ehEdicao) {
      validarInteiroPositivo(erros, "id", controles.id.obterValor());
    }
    validarTextoObrigatorio(erros, "nome", controles.nome.value);
    validarTextoObrigatorio(erros, "responsavel", controles.responsavel.value);
    validarEscolha(erros, "setor", controles.setor.obterValor());
    validarEscolha(erros, "status", controles.status.obterValor());
    if (tipoEscolhido !== null) {
      validarCamposDoTipo(erros, tipoEscolhido, controles);
    }
    return erros;
  }

  function mostrarErros(erros) {
    const errosDosCampos = [];
    for (const erro of erros) {
      if (erro.campo === "tipo") {
        mostrarAjuda(escolhaDeTipo.textoDeAjuda, erro.mensagem, true);
      } else {
        errosDosCampos.push(erro);
      }
    }
    if (errosDosCampos.length > 0) {
      mostrarErrosNasLinhas(errosDosCampos, linhas);
    }
    if (erros[0].campo === "tipo") {
      escolhaDeTipo.elemento.querySelector("input").focus();
    }
  }

  function limparErros() {
    mostrarAjuda(escolhaDeTipo.textoDeAjuda, "");
    for (const linha of Object.values(linhas)) {
      linha.limparErro();
    }
    mostrarAjudaDoFator();
  }

  function montarDadosParaAApi() {
    const dados = {
      tipo: tipoEscolhido,
      nome: controles.nome.value.trim(),
      responsavel: controles.responsavel.value.trim(),
      setor: controles.setor.obterValor(),
      status: controles.status.obterValor(),
      fator_exposicao: controles.fator.obterValor(),
      ...montarCamposDoTipo(tipoEscolhido, controles),
    };
    if (!ehEdicao) {
      dados.id = controles.id.obterValor();
    }
    return dados;
  }

  return { elemento, validar, mostrarErros, limparErros, montarDadosParaAApi };
}

function criarControles(opcoes, ativo) {
  const valores = ativo ?? {};
  return {
    id: criarCampoDeNumero({ nome: "id", inteiro: true, textoDeExemplo: "Ex.: 7" }),
    nome: criarCampoDeTexto({
      nome: "nome",
      valor: valores.nome ?? "",
      textoDeExemplo: "Ex.: Notebook do Rafael",
      tamanhoMaximo: 80,
    }),
    responsavel: criarCampoDeTexto({
      nome: "responsavel",
      valor: valores.responsavel ?? "",
      textoDeExemplo: "Ex.: Rafael Torres",
      tamanhoMaximo: 80,
    }),
    setor: criarMenuSuspenso({
      rotulo: "Setor",
      opcoes: opcoes.setores,
      valor: valores.setor ?? null,
      textoQuandoVazio: "Escolha o setor",
    }),
    status: criarMenuSuspenso({
      rotulo: "Status",
      opcoes: opcoes.statusDoAtivo,
      valor: valores.status ?? null,
      textoQuandoVazio: "Escolha o status",
    }),
    fator: criarControleDeslizante({
      minimo: MENOR_FATOR,
      maximo: MAIOR_FATOR,
      passo: 0.1,
      valor: valores.fator_exposicao ?? 1,
      formatar: formatarNumero,
    }),
    sistemaOperacional: criarCampoDeTexto({
      nome: "sistema_operacional",
      valor: valores.sistema_operacional ?? "",
      textoDeExemplo: "Ex.: Linux",
      tamanhoMaximo: 60,
    }),
    tela: criarCampoDeNumero({ nome: "tela", valor: valores.tela ?? null, unidade: "polegadas" }),
    ram: criarContador({ rotulo: "Memória RAM", valor: valores.ram ?? 8, unidade: "GB" }),
    armazenamento: criarCampoDeNumero({
      nome: "armazenamento",
      valor: valores.armazenamento ?? null,
      unidade: "TB",
    }),
    portas: criarContador({ rotulo: "Portas", valor: valores.portas ?? 8 }),
    velocidade: criarCampoDeNumero({
      nome: "velocidade",
      valor: valores.velocidade ?? null,
      unidade: "MB",
      inteiro: true,
    }),
    cor: criarMenuSuspenso({
      rotulo: "Cor",
      opcoes: opcoes.coresDeImpressora,
      valor: valores.cor ?? null,
      textoQuandoVazio: "Escolha a cor",
    }),
    tecnologia: criarMenuSuspenso({
      rotulo: "Tecnologia",
      opcoes: opcoes.tecnologiasDeImpressora,
      valor: valores.tecnologia ?? null,
      textoQuandoVazio: "Escolha a tecnologia",
    }),
  };
}

function criarLinhas(controles, ehEdicao) {
  const linhas = {
    nome: criarLinhaComValidacao({
      rotulo: "Nome",
      controle: controles.nome,
      ajuda: "Como o ativo aparece nas listas",
    }),
    responsavel: criarLinhaComValidacao({ rotulo: "Responsável", controle: controles.responsavel }),
    setor: criarLinhaComValidacao({ rotulo: "Setor", controle: controles.setor.elemento }),
    status: criarLinhaComValidacao({ rotulo: "Status", controle: controles.status.elemento }),
    fator: criarLinhaComValidacao({
      rotulo: "Fator de exposição",
      controle: controles.fator.elemento,
      alvoDoRotulo: controles.fator.campo,
      explicacaoDoConceito:
        "O fator de exposição multiplica o risco próprio do ativo: quanto mais exposto à rede, " +
        "maior ele é. Vai de 0,1 a 2 e começa no padrão do tipo.",
    }),
    sistemaOperacional: criarLinhaComValidacao({
      rotulo: "Sistema operacional",
      controle: controles.sistemaOperacional,
    }),
    tela: criarLinhaDeControleComposto("Tela", controles.tela),
    ram: criarLinhaDeControleComposto("Memória RAM", controles.ram),
    armazenamento: criarLinhaDeControleComposto("Armazenamento", controles.armazenamento),
    portas: criarLinhaDeControleComposto("Portas", controles.portas),
    velocidade: criarLinhaDeControleComposto("Velocidade", controles.velocidade),
    cor: criarLinhaComValidacao({ rotulo: "Cor", controle: controles.cor.elemento }),
    tecnologia: criarLinhaComValidacao({
      rotulo: "Tecnologia",
      controle: controles.tecnologia.elemento,
    }),
  };
  if (!ehEdicao) {
    linhas.id = criarLinhaComValidacao({
      rotulo: "ID",
      controle: controles.id.elemento,
      alvoDoRotulo: controles.id.campo,
      ajuda: "Número inteiro que identifica o ativo",
    });
  }
  return linhas;
}

function criarLinhaDeControleComposto(rotulo, controleComposto) {
  return criarLinhaComValidacao({
    rotulo: rotulo,
    controle: controleComposto.elemento,
    alvoDoRotulo: controleComposto.campo,
  });
}

function criarEscolhaDeTipo(tipos, tipoInicial, aoEscolher) {
  const nomeDoGrupo = gerarIdentificador("tipo");
  const textoDeAjuda = criarElemento("p", {
    classe: "ajuda-de-campo",
    id: gerarIdentificador("ajuda"),
    hidden: true,
  });
  const blocos = criarElemento("div", {
    classe: "blocos-de-tipo",
    role: "radiogroup",
    "aria-label": "Tipo do ativo",
    "aria-describedby": textoDeAjuda.id,
  });
  for (const tipo of tipos) {
    const entrada = criarElemento("input", {
      type: "radio",
      classe: "visualmente-oculto",
      name: nomeDoGrupo,
      value: tipo.valor,
      checked: tipo.valor === tipoInicial,
    });
    entrada.addEventListener("change", () => aoEscolher(tipo.valor));
    blocos.append(
      criarElemento("label", { classe: "bloco-de-tipo" }, [
        entrada,
        criarIcone(tipo.icone),
        criarElemento("span", { texto: tipo.rotulo }),
      ]),
    );
  }
  return { elemento: blocos, textoDeAjuda };
}

function validarCamposDoTipo(erros, tipo, controles) {
  if (tipo === "Notebook") {
    validarTextoObrigatorio(erros, "sistemaOperacional", controles.sistemaOperacional.value);
    validarNumeroPositivo(erros, "tela", controles.tela.obterValor());
  } else if (tipo === "Servidor") {
    validarNumeroPositivo(erros, "armazenamento", controles.armazenamento.obterValor());
  } else if (tipo === "Roteador") {
    validarInteiroPositivo(erros, "velocidade", controles.velocidade.obterValor());
  } else if (tipo === "Impressora") {
    validarEscolha(erros, "cor", controles.cor.obterValor());
    validarEscolha(erros, "tecnologia", controles.tecnologia.obterValor());
  }
}

function montarCamposDoTipo(tipo, controles) {
  if (tipo === "Notebook") {
    return {
      sistema_operacional: controles.sistemaOperacional.value.trim(),
      tela: controles.tela.obterValor(),
    };
  }
  if (tipo === "Servidor") {
    return { ram: controles.ram.obterValor(), armazenamento: controles.armazenamento.obterValor() };
  }
  if (tipo === "Roteador") {
    return { portas: controles.portas.obterValor(), velocidade: controles.velocidade.obterValor() };
  }
  return { cor: controles.cor.obterValor(), tecnologia: controles.tecnologia.obterValor() };
}
