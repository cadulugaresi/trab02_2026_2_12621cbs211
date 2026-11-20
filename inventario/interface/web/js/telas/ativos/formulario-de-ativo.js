import { buscarAtivo, cadastrarAtivo, editarAtivo } from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { criarBotao, liberarBotao, marcarBotaoComoOcupado } from "../../componentes/botoes.js";
import {
  criarCampoDeNumero,
  criarCampoDeTexto,
  criarLinhaDeCampo,
  mostrarAjuda,
} from "../../componentes/campos.js";
import { criarContador } from "../../componentes/contador.js";
import { criarControleDeslizante } from "../../componentes/controle-deslizante.js";
import { criarFaixaDeErro } from "../../componentes/faixa-de-erro.js";
import { criarMenuSuspenso } from "../../componentes/menu-suspenso.js";
import { criarElemento, gerarIdentificador } from "../../elementos.js";
import { formatarNumero } from "../../formatos.js";
import { criarIcone } from "../../icones.js";
import { carregarOpcoes, encontrarOpcao } from "../../opcoes.js";
import { trocarEnderecoPor, voltarOuIrPara } from "../../roteador.js";
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
  const enderecoDeVolta = ehEdicao ? `/ativos/${idEmEdicao}` : "/ativos";
  const faixa = criarFaixaDeErro();
  const subtitulo = criarElemento("p", { classe: "texto-de-apoio" });
  const areaDosCampos = criarElemento("div", { classe: "campos-do-formulario" });
  const botaoDeSalvar = criarBotao({ texto: "Salvar ativo" });
  botaoDeSalvar.type = "submit";
  botaoDeSalvar.disabled = true;

  const formulario = criarElemento("form", { classe: "formulario-de-ajustes", novalidate: true }, [
    criarElemento("header", { classe: "cabecalho-do-formulario" }, [
      criarElemento("div", { classe: "cabecalho-de-tela-textos" }, [
        criarElemento("h1", {
          classe: "titulo-de-tela",
          texto: ehEdicao ? "Editar ativo" : "Novo ativo",
        }),
        subtitulo,
      ]),
      criarElemento("div", { classe: "cabecalho-do-formulario-botoes" }, [
        criarBotao({
          texto: "Cancelar",
          variacao: "secundario",
          aoClicar: () => voltarOuIrPara(enderecoDeVolta),
        }),
        botaoDeSalvar,
      ]),
    ]),
    faixa.elemento,
    areaDosCampos,
  ]);
  tela.append(formulario);

  Promise.all([carregarOpcoes(), ehEdicao ? buscarAtivo(idEmEdicao) : null])
    .then(([opcoes, ativo]) => {
      const campos = criarCampos(opcoes, ativo);
      areaDosCampos.append(campos.elemento);
      subtitulo.textContent = ehEdicao
        ? `ID ${ativo.id} · ${ativo.nome}`
        : "Escolha o tipo e preencha os dados do ativo";
      botaoDeSalvar.disabled = false;
      formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        salvar(campos, idEmEdicao, faixa, botaoDeSalvar);
      });
    })
    .catch((erro) => faixa.mostrar(erro.message));
}

async function salvar(campos, idEmEdicao, faixa, botaoDeSalvar) {
  faixa.esconder();
  campos.limparErros();
  const erros = campos.validar();
  if (erros.length > 0) {
    campos.mostrarErros(erros);
    return;
  }

  const dadosDoAtivo = campos.montarDadosParaAApi();
  marcarBotaoComoOcupado(botaoDeSalvar, "Salvando…");
  try {
    const ativoSalvo =
      idEmEdicao === null
        ? await cadastrarAtivo(dadosDoAtivo)
        : await editarAtivo(idEmEdicao, dadosDoAtivo);
    mostrarAvisoDeSucesso(idEmEdicao === null ? "Ativo cadastrado" : "Ativo atualizado");
    trocarEnderecoPor(`/ativos/${ativoSalvo.id}`);
  } catch (erro) {
    liberarBotao(botaoDeSalvar);
    faixa.mostrar(erro.message);
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

  const gruposDeIdentificacao = ehEdicao
    ? [linhas.nome.elemento, linhas.responsavel.elemento]
    : [linhas.id.elemento, linhas.nome.elemento, linhas.responsavel.elemento];

  const elemento = criarElemento("div", {}, [
    criarGrupo("Tipo", [escolhaDeTipo.elemento, escolhaDeTipo.textoDeAjuda]),
    criarGrupo("Identificação", gruposDeIdentificacao),
    criarGrupo("Situação", [linhas.setor.elemento, linhas.status.elemento]),
    criarGrupo("Exposição", [linhas.fator.elemento]),
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
    for (const erro of erros) {
      if (erro.campo === "tipo") {
        mostrarAjuda(escolhaDeTipo.textoDeAjuda, erro.mensagem, true);
        continue;
      }
      linhas[erro.campo].alvo.setAttribute("aria-invalid", "true");
      mostrarAjuda(linhas[erro.campo].textoDeAjuda, erro.mensagem, true);
    }
    focarPrimeiroErro(erros, linhas, escolhaDeTipo);
  }

  function limparErros() {
    mostrarAjuda(escolhaDeTipo.textoDeAjuda, "");
    for (const linha of Object.values(linhas)) {
      linha.alvo.removeAttribute("aria-invalid");
      mostrarAjuda(linha.textoDeAjuda, linha.ajudaPadrao);
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
  const nome = criarCampoDeTexto({
    nome: "nome",
    valor: valores.nome ?? "",
    textoDeExemplo: "Ex.: Notebook do Rafael",
    tamanhoMaximo: 80,
  });
  const responsavel = criarCampoDeTexto({
    nome: "responsavel",
    valor: valores.responsavel ?? "",
    textoDeExemplo: "Ex.: Rafael Torres",
    tamanhoMaximo: 80,
  });
  const sistemaOperacional = criarCampoDeTexto({
    nome: "sistema_operacional",
    valor: valores.sistema_operacional ?? "",
    textoDeExemplo: "Ex.: Linux",
    tamanhoMaximo: 60,
  });

  return {
    id: criarCampoDeNumero({ nome: "id", inteiro: true, textoDeExemplo: "Ex.: 7" }),
    nome: nome,
    responsavel: responsavel,
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
    sistemaOperacional: sistemaOperacional,
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
    nome: criarLinha("Nome", controles.nome, controles.nome, "Como o ativo aparece nas listas"),
    responsavel: criarLinha("Responsável", controles.responsavel, controles.responsavel, ""),
    setor: criarLinha("Setor", controles.setor.elemento, controles.setor.elemento, ""),
    status: criarLinha("Status", controles.status.elemento, controles.status.elemento, ""),
    fator: criarLinha("Fator de exposição", controles.fator.elemento, controles.fator.campo, "", {
      explicacaoDoConceito:
        "O fator de exposição multiplica o risco próprio do ativo: quanto mais exposto à rede, " +
        "maior ele é. Vai de 0,1 a 2 e começa no padrão do tipo.",
    }),
    sistemaOperacional: criarLinha(
      "Sistema operacional",
      controles.sistemaOperacional,
      controles.sistemaOperacional,
      "",
    ),
    tela: criarLinha("Tela", controles.tela.elemento, controles.tela.campo, ""),
    ram: criarLinha("Memória RAM", controles.ram.elemento, controles.ram.campo, ""),
    armazenamento: criarLinha(
      "Armazenamento",
      controles.armazenamento.elemento,
      controles.armazenamento.campo,
      "",
    ),
    portas: criarLinha("Portas", controles.portas.elemento, controles.portas.campo, ""),
    velocidade: criarLinha("Velocidade", controles.velocidade.elemento, controles.velocidade.campo, ""),
    cor: criarLinha("Cor", controles.cor.elemento, controles.cor.elemento, ""),
    tecnologia: criarLinha("Tecnologia", controles.tecnologia.elemento, controles.tecnologia.elemento, ""),
  };
  if (!ehEdicao) {
    linhas.id = criarLinha(
      "ID",
      controles.id.elemento,
      controles.id.campo,
      "Número inteiro que identifica o ativo",
    );
  }
  return linhas;
}

function criarLinha(rotulo, controle, alvo, ajudaPadrao, extras = {}) {
  const linha = criarLinhaDeCampo({
    rotulo: rotulo,
    controle: controle,
    alvoDoRotulo: alvo,
    ajuda: ajudaPadrao,
    explicacaoDoConceito: extras.explicacaoDoConceito,
  });

  function tirarErroDoCampo() {
    if (alvo.getAttribute("aria-invalid") === "true") {
      alvo.removeAttribute("aria-invalid");
      mostrarAjuda(linha.textoDeAjuda, ajudaPadrao);
    }
  }

  linha.elemento.addEventListener("input", tirarErroDoCampo);
  linha.elemento.addEventListener("change", tirarErroDoCampo);
  return { ...linha, alvo, ajudaPadrao };
}

function criarGrupo(titulo, filhos) {
  return criarElemento("section", { classe: "grupo-de-ajustes" }, [
    criarElemento("h2", { classe: "titulo-de-secao", texto: titulo }),
    ...filhos,
  ]);
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

function validarTextoObrigatorio(erros, campo, texto) {
  const textoLimpo = texto.trim();
  if (textoLimpo === "") {
    erros.push({ campo, mensagem: "Este campo não pode ser vazio" });
  } else if (/^\d+$/.test(textoLimpo)) {
    erros.push({ campo, mensagem: "Este campo não pode ser composto apenas por números" });
  }
}

function validarEscolha(erros, campo, valor) {
  if (valor === null) {
    erros.push({ campo, mensagem: "Escolha uma opção" });
  }
}

function validarNumeroPositivo(erros, campo, numero) {
  if (numero === null || numero <= 0) {
    erros.push({ campo, mensagem: "Digite um número maior que zero" });
  }
}

function validarInteiroPositivo(erros, campo, numero) {
  if (numero === null || numero <= 0) {
    erros.push({ campo, mensagem: "Digite um número inteiro maior que zero" });
  }
}

function focarPrimeiroErro(erros, linhas, escolhaDeTipo) {
  const primeiroErro = erros[0];
  if (primeiroErro.campo === "tipo") {
    escolhaDeTipo.elemento.querySelector("input").focus();
    return;
  }
  linhas[primeiroErro.campo].alvo.focus();
}
