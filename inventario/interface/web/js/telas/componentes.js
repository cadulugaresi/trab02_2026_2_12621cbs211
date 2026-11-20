import { buscarAtivo } from "../api.js";
import { mostrarAvisoDeSucesso } from "../componentes/aviso-de-sucesso.js";
import { abrirBalaoDeExclusao } from "../componentes/balao-de-exclusao.js";
import { criarBotao } from "../componentes/botoes.js";
import {
  AJUDA_DO_CVSS,
  EXPLICACAO_DO_CVSS,
  criarCampoDeCvss,
} from "../componentes/campo-de-cvss.js";
import { criarCampoDeTexto, criarLinhaDeCampo, mostrarAjuda } from "../componentes/campos.js";
import { criarContador } from "../componentes/contador.js";
import { criarFaixaDeErro } from "../componentes/faixa-de-erro.js";
import { criarMenuComBusca } from "../componentes/menu-com-busca.js";
import { criarMenuSuspenso } from "../componentes/menu-suspenso.js";
import {
  criarPilulaDeStatus,
  criarPilulaDeStatusTrocavel,
} from "../componentes/pilula-de-status.js";
import { criarSegmentado } from "../componentes/segmentado.js";
import { criarElemento, gerarIdentificador } from "../elementos.js";
import { carregarOpcoes } from "../opcoes.js";
import { navegarPara } from "../roteador.js";

const ATIVOS_DE_EXEMPLO = [
  { valor: 1, rotulo: "Notebook do Rafael" },
  { valor: 2, rotulo: "Roteador do escritório" },
  { valor: 3, rotulo: "Servidor web" },
  { valor: 4, rotulo: "Impressora do RH" },
  { valor: 5, rotulo: "Servidor de arquivos" },
];

const VULNERABILIDADES_DE_EXEMPLO = [
  { valor: 1, rotulo: "Log4Shell" },
  { valor: 2, rotulo: "Senha padrão no painel" },
  { valor: 3, rotulo: "Heartbleed" },
  { valor: 4, rotulo: "EternalBlue" },
];

const ID_DE_ATIVO_QUE_NAO_EXISTE = 999999;

export function montarTelaDeComponentes(tela) {
  const faixaDasOpcoes = criarFaixaDeErro();
  const vitrineDosMenus = criarVitrineDosMenus();
  const vitrineDasPilulas = criarVitrineDasPilulas();

  tela.append(
    criarCabecalho(),
    faixaDasOpcoes.elemento,
    criarVitrineDosBotoes(),
    criarVitrineDoSegmentado(),
    criarVitrineDoContador(),
    criarVitrineDosCampos(),
    vitrineDosMenus.elemento,
    criarVitrineDoMenuComBusca(),
    criarVitrineDoCvss(),
    vitrineDasPilulas.elemento,
    criarVitrineDaJanela(),
    criarVitrineDosAvisos(),
    criarVitrineDaFaixaDeErro(),
  );

  carregarOpcoes()
    .then((opcoes) => {
      vitrineDosMenus.preencher(opcoes);
      vitrineDasPilulas.preencher(opcoes);
    })
    .catch((erro) => faixaDasOpcoes.mostrar(erro.message));
}

function criarCabecalho() {
  return criarElemento("header", { classe: "cabecalho-de-tela" }, [
    criarElemento("h1", { classe: "titulo-de-tela", texto: "Componentes" }),
    criarElemento("p", {
      classe: "texto-de-apoio",
      texto:
        "As peças da interface, cada uma funcionando, para revisar o visual antes das telas. " +
        "Nada aqui grava dados: os menus de setor e de status leem GET /opcoes e a faixa de erro " +
        "faz uma consulta de leitura.",
    }),
  ]);
}

function criarVitrine(titulo, explicacao, exemplos) {
  const identificadorDoTitulo = gerarIdentificador("vitrine");
  return criarElemento("section", { classe: "vitrine", "aria-labelledby": identificadorDoTitulo }, [
    criarElemento("div", { classe: "vitrine-explicacao" }, [
      criarElemento("h2", {
        classe: "titulo-de-secao",
        id: identificadorDoTitulo,
        texto: titulo,
      }),
      criarElemento("p", { classe: "texto-de-apoio", texto: explicacao }),
    ]),
    criarElemento("div", { classe: "vitrine-exemplos" }, exemplos),
  ]);
}

function criarLinha(filhos) {
  return criarElemento("div", { classe: "vitrine-linha" }, filhos);
}

function criarVitrineDosBotoes() {
  const botaoDesativado = criarBotao({ texto: "Salvar ativo" });
  botaoDesativado.disabled = true;

  return criarVitrine(
    "Botões",
    "Um botão principal por área. Encolhem um pouco ao pressionar.",
    [
      criarLinha([
        criarBotao({ texto: "Salvar ativo" }),
        criarBotao({ texto: "Cancelar", variacao: "secundario" }),
        criarBotao({ texto: "Excluir", variacao: "perigo" }),
      ]),
      criarLinha([
        criarBotao({ texto: "Editar", variacao: "secundario", icone: "editar", pequeno: true }),
        criarBotao({ variacao: "icone", icone: "fechar", rotuloAcessivel: "Fechar" }),
        botaoDesativado,
        criarBotao({ texto: "Ver ranking", variacao: "link", iconeDepois: "avancar" }),
      ]),
    ],
  );
}

function criarVitrineDoSegmentado() {
  const resultadoDaOrdem = criarElemento("p", { classe: "vitrine-resultado" });
  const resultadoDoModo = criarElemento("p", { classe: "vitrine-resultado" });
  const resultadoDoAgrupamento = criarElemento("p", { classe: "vitrine-resultado" });
  const nomesDaOrdem = { id: "ID", nome: "Nome", vulnerabilidades: "Vulnerabilidades" };

  function mostrarResultado(elemento, texto) {
    elemento.replaceChildren("Escolhido: ", criarElemento("strong", { texto: texto }));
  }

  const ordenacao = criarSegmentado({
    rotulo: "Ordenar por",
    valor: "id",
    opcoes: [
      { valor: "id", rotulo: "ID" },
      { valor: "nome", rotulo: "Nome" },
      { valor: "vulnerabilidades", rotulo: "Vulnerabilidades" },
    ],
    aoMudar: (valor) => mostrarResultado(resultadoDaOrdem, nomesDaOrdem[valor]),
  });
  const trocaDeModo = criarSegmentado({
    rotulo: "Modo de exibição",
    variacao: "troca-de-modo",
    valor: "lista",
    opcoes: [
      { valor: "lista", rotulo: "Lista" },
      { valor: "mapa", rotulo: "Mapa" },
    ],
    aoMudar: (valor) => mostrarResultado(resultadoDoModo, valor === "lista" ? "Lista" : "Mapa"),
  });
  const agrupamento = criarSegmentado({
    rotulo: "Agrupar vínculos",
    variacao: "troca-de-modo",
    valor: "ativo",
    opcoes: [
      { valor: "ativo", rotulo: "Por ativo" },
      { valor: "vulnerabilidade", rotulo: "Por vulnerabilidade" },
    ],
    aoMudar: (valor) =>
      mostrarResultado(
        resultadoDoAgrupamento,
        valor === "ativo" ? "Por ativo" : "Por vulnerabilidade",
      ),
  });

  mostrarResultado(resultadoDaOrdem, "ID");
  mostrarResultado(resultadoDoModo, "Lista");
  mostrarResultado(resultadoDoAgrupamento, "Por ativo");

  return criarVitrine(
    "Controle segmentado",
    "O padrão serve para filtros e ordenação. A troca de modo, com o cartão preto, muda a forma " +
      "de ver a mesma informação. Também funciona com as setas do teclado.",
    [
      criarElemento("div", { classe: "vitrine-segmentado" }, [
        ordenacao.elemento,
        resultadoDaOrdem,
      ]),
      criarElemento("div", { classe: "vitrine-segmentado" }, [
        trocaDeModo.elemento,
        resultadoDoModo,
      ]),
      criarElemento("div", { classe: "vitrine-segmentado" }, [
        agrupamento.elemento,
        resultadoDoAgrupamento,
      ]),
    ],
  );
}

function criarVitrineDoContador() {
  const portas = criarContador({ rotulo: "Portas", valor: 8, maximo: 512 });
  const memoria = criarContador({ rotulo: "Memória RAM", valor: 16, maximo: 4096, unidade: "GB" });

  return criarVitrine(
    "Contador",
    "Para números inteiros, como portas e memória. Clique no número para digitar por cima.",
    [
      criarElemento("div", { classe: "vitrine-grade-de-campos" }, [
        criarLinhaDeCampo({
          rotulo: "Portas",
          controle: portas.elemento,
          alvoDoRotulo: portas.campo,
          ajuda: "De 1 a 512",
        }).elemento,
        criarLinhaDeCampo({
          rotulo: "Memória RAM",
          controle: memoria.elemento,
          alvoDoRotulo: memoria.campo,
          ajuda: "As setas do teclado também mudam o valor",
        }).elemento,
      ]),
    ],
  );
}

function criarVitrineDosCampos() {
  const campoDeSistema = criarCampoDeTexto({ nome: "sistema_operacional", obrigatorio: true });
  const linhaDoSistema = criarLinhaDeCampo({ rotulo: "Sistema operacional", controle: campoDeSistema });
  campoDeSistema.setAttribute("aria-invalid", "true");
  mostrarAjuda(linhaDoSistema.textoDeAjuda, "Este campo não pode ser vazio.", true);
  campoDeSistema.addEventListener("input", () => {
    const vazio = campoDeSistema.value.trim() === "";
    campoDeSistema.toggleAttribute("aria-invalid", vazio);
    mostrarAjuda(
      linhaDoSistema.textoDeAjuda,
      vazio ? "Este campo não pode ser vazio." : "Ex.: Linux, Windows 11",
      vazio,
    );
  });

  return criarVitrine(
    "Campos",
    "Pílulas cinza, sem borda. O foco ganha contorno preto. O campo com erro fica em destaque " +
      "e a ajuda embaixo diz o que corrigir.",
    [
      criarElemento("div", { classe: "vitrine-grade-de-campos" }, [
        criarLinhaDeCampo({
          rotulo: "Nome",
          controle: criarCampoDeTexto({
            nome: "nome",
            textoDeExemplo: "Ex.: Notebook do Rafael",
            obrigatorio: true,
          }),
          ajuda: "Como o ativo aparece nas listas",
        }).elemento,
        criarLinhaDeCampo({
          rotulo: "Responsável",
          controle: criarCampoDeTexto({ nome: "responsavel", valor: "Rafael Torres" }),
        }).elemento,
        linhaDoSistema.elemento,
      ]),
    ],
  );
}

function criarVitrineDosMenus() {
  const setor = criarMenuSuspenso({ rotulo: "Setor", textoQuandoVazio: "Carregando…" });
  const status = criarMenuSuspenso({ rotulo: "Status do ativo", textoQuandoVazio: "Carregando…" });

  const elemento = criarVitrine(
    "Menu suspenso",
    "Abre embaixo do campo, saindo dele. As opções de setor e de status vêm de GET /opcoes.",
    [
      criarElemento("div", { classe: "vitrine-grade-de-campos" }, [
        criarLinhaDeCampo({ rotulo: "Setor", controle: setor.elemento }).elemento,
        criarLinhaDeCampo({ rotulo: "Status", controle: status.elemento }).elemento,
      ]),
    ],
  );

  function preencher(opcoes) {
    setor.definirOpcoes(opcoes.setores);
    setor.definirValor(opcoes.setores[0].valor);
    status.definirOpcoes(opcoes.statusDoAtivo);
    status.definirValor(opcoes.statusDoAtivo[0].valor);
  }

  return { elemento, preencher };
}

function criarVitrineDoMenuComBusca() {
  const ativo = criarMenuComBusca({
    rotulo: "Ativo",
    itens: ATIVOS_DE_EXEMPLO,
    textoQuandoVazio: "Escolha um ativo",
    textoSemResultado: "Nenhum ativo com esse nome ou ID",
  });
  const vulnerabilidade = criarMenuComBusca({
    rotulo: "Vulnerabilidade",
    itens: VULNERABILIDADES_DE_EXEMPLO,
    valor: 1,
    textoQuandoVazio: "Escolha uma vulnerabilidade",
    textoSemResultado: "Nenhuma vulnerabilidade com esse nome ou ID",
  });

  return criarVitrine(
    "Menu com busca",
    "Para escolher um ativo ou uma vulnerabilidade. Busca por nome ou ID; cada item mostra os dois.",
    [
      criarElemento("div", { classe: "vitrine-grade-de-campos" }, [
        criarLinhaDeCampo({ rotulo: "Ativo", controle: ativo.elemento }).elemento,
        criarLinhaDeCampo({ rotulo: "Vulnerabilidade", controle: vulnerabilidade.elemento })
          .elemento,
      ]),
    ],
  );
}

function criarVitrineDoCvss() {
  const cvss = criarCampoDeCvss({ valor: 9.8 });
  const linha = criarLinhaDeCampo({
    rotulo: "CVSS",
    controle: cvss.elemento,
    alvoDoRotulo: cvss.campo,
    ajuda: AJUDA_DO_CVSS,
    explicacaoDoConceito: EXPLICACAO_DO_CVSS,
  });
  cvss.ligarTextoDeAjuda(linha.textoDeAjuda);

  const amostras = [];
  for (const valor of [2.5, 5.3, 7.5, 9.8]) {
    const amostra = criarCampoDeCvss({ valor: valor });
    amostra.campo.readOnly = true;
    amostra.campo.tabIndex = -1;
    amostra.campo.setAttribute("aria-label", "Amostra de CVSS");
    amostras.push(amostra.elemento);
  }

  return criarVitrine(
    "Campo de CVSS",
    "O fundo assume a cor do nível enquanto você digita. Fora de 0,1 a 10, volta ao cinza e avisa.",
    [
      criarElemento("div", { classe: "vitrine-formulario" }, [linha.elemento]),
      criarElemento("div", { classe: "vitrine-amostras" }, amostras),
    ],
  );
}

function criarVitrineDasPilulas() {
  const linhaDoAtivo = criarLinha([]);
  const linhaDoTratamento = criarLinha([]);

  const elemento = criarVitrine(
    "Pílulas de status",
    "A pílula é neutra; só a bolinha tem cor. A de tratamento abre um menu para trocar ali mesmo.",
    [
      criarElemento("div", { classe: "vitrine-legenda-de-pilulas" }, [
        criarElemento("p", { classe: "legenda", texto: "Status do ativo" }),
        linhaDoAtivo,
      ]),
      criarElemento("div", { classe: "vitrine-legenda-de-pilulas" }, [
        criarElemento("p", { classe: "legenda", texto: "Status de tratamento (clique para trocar)" }),
        linhaDoTratamento,
      ]),
    ],
  );

  function preencher(opcoes) {
    for (const opcao of opcoes.statusDoAtivo) {
      linhaDoAtivo.append(criarPilulaDeStatus({ rotulo: opcao.rotulo, cor: opcao.cor }));
    }
    for (const opcao of opcoes.statusDeTratamento) {
      const pilula = criarPilulaDeStatusTrocavel({
        rotulo: "Status de tratamento",
        opcoes: opcoes.statusDeTratamento,
        valor: opcao.valor,
      });
      linhaDoTratamento.append(pilula.elemento);
    }
  }

  return { elemento, preencher };
}

function criarVitrineDaJanela() {
  return criarVitrine(
    "Janela de detalhes",
    "Abre por cima do véu, com rota própria. Fecha com Esc, clique fora, × ou o Voltar do navegador.",
    [
      criarBotao({
        texto: "Abrir a janela de exemplo",
        variacao: "secundario",
        aoClicar: () => navegarPara("/componentes/janela"),
      }),
    ],
  );
}

function criarVitrineDosAvisos() {
  const botaoDeExcluir = criarBotao({ texto: "Excluir", variacao: "secundario", icone: "excluir" });
  botaoDeExcluir.addEventListener("click", () => {
    abrirBalaoDeExclusao({
      ancora: botaoDeExcluir,
      pergunta: "Excluir Servidor web?",
      explicacao: "Os vínculos e as dependências dele também serão removidos.",
      aoConfirmar: () => mostrarAvisoDeSucesso("Ativo excluído"),
    });
  });

  return criarVitrine(
    "Balão de exclusão e aviso",
    "O balão sai do próprio botão Excluir. O aviso de sucesso sobe perto do Cadastrar e some " +
      "sozinho em 3 segundos. Aqui é só demonstração: nada é excluído.",
    [
      criarLinha([
        botaoDeExcluir,
        criarBotao({
          texto: "Mostrar aviso de sucesso",
          variacao: "secundario",
          aoClicar: () => mostrarAvisoDeSucesso("Ativo cadastrado"),
        }),
      ]),
    ],
  );
}

function criarVitrineDaFaixaDeErro() {
  const faixa = criarFaixaDeErro();
  const botaoDeConsultar = criarBotao({
    texto: `Buscar o ativo ${ID_DE_ATIVO_QUE_NAO_EXISTE}`,
    variacao: "secundario",
  });
  botaoDeConsultar.addEventListener("click", async () => {
    faixa.esconder();
    try {
      await buscarAtivo(ID_DE_ATIVO_QUE_NAO_EXISTE);
    } catch (erro) {
      faixa.mostrar(erro.message);
    }
  });

  return criarVitrine(
    "Faixa de erro",
    'Fica no topo do formulário e mostra a mensagem que a API devolve em {"erro": ...}. ' +
      "O botão faz uma consulta de verdade a um ativo que não existe.",
    [
      criarElemento("div", { classe: "vitrine-formulario" }, [
        faixa.elemento,
        criarLinha([botaoDeConsultar]),
      ]),
    ],
  );
}
