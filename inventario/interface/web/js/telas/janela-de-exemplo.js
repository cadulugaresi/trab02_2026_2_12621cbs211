import { mostrarAvisoDeSucesso } from "../componentes/aviso-de-sucesso.js";
import { abrirBalaoDeExclusao } from "../componentes/balao-de-exclusao.js";
import { criarBotao } from "../componentes/botoes.js";
import { criarFaixaDeErro } from "../componentes/faixa-de-erro.js";
import { abrirJanela } from "../componentes/janela.js";
import { criarNumeroAnimado } from "../componentes/numero-animado.js";
import { criarPilulaDeStatusTrocavel } from "../componentes/pilula-de-status.js";
import { criarElemento } from "../elementos.js";
import { formatarCvss, formatarRisco } from "../formatos.js";
import { carregarOpcoes } from "../opcoes.js";
import { navegarPara } from "../roteador.js";
import { NIVEIS_DE_GRAVIDADE } from "../rotulos.js";

const ATIVO_DE_EXEMPLO = {
  id: 3,
  nome: "Servidor web",
  descricao: "Servidor · TI · Rafael Torres",
  fatorDeExposicao: 1.3,
  riscoHerdado: 3.41,
  vulnerabilidades: [
    { id: 1, nome: "Log4Shell", cvss: 10, nivel: "CRITICO", statusDeTratamento: 1 },
    { id: 2, nome: "Senha padrão no painel", cvss: 7.5, nivel: "ALTO", statusDeTratamento: 2 },
  ],
};

export function abrirJanelaDeExemplo(parametros, { pedirFechamento }) {
  const vinculos = copiarVinculosDoExemplo();
  const riscos = criarNumerosDeRisco(
    calcularRiscoProprio(vinculos, null),
    ATIVO_DE_EXEMPLO.riscoHerdado,
  );
  const corpo = criarElemento("div", {}, [riscos.elemento]);

  abrirJanela({
    titulo: ATIVO_DE_EXEMPLO.nome,
    subtitulo: ATIVO_DE_EXEMPLO.descricao,
    acoes: criarAcoesDaJanela(pedirFechamento),
    corpo: corpo,
    aoPedirFechamento: pedirFechamento,
  });

  carregarOpcoes()
    .then((opcoes) => {
      const valorDeCorrigida = encontrarValorDeCorrigida(opcoes.statusDeTratamento);
      function recalcularRiscos() {
        riscos.animarAte(
          calcularRiscoProprio(vinculos, valorDeCorrigida),
          ATIVO_DE_EXEMPLO.riscoHerdado,
        );
      }
      corpo.append(criarListaDeVinculos(vinculos, opcoes.statusDeTratamento, recalcularRiscos));
    })
    .catch((erro) => {
      const faixa = criarFaixaDeErro();
      corpo.append(faixa.elemento);
      faixa.mostrar(erro.message);
    });
}

function copiarVinculosDoExemplo() {
  const vinculos = [];
  for (const vulnerabilidade of ATIVO_DE_EXEMPLO.vulnerabilidades) {
    vinculos.push({ ...vulnerabilidade });
  }
  return vinculos;
}

function encontrarValorDeCorrigida(opcoesDeStatus) {
  for (const opcao of opcoesDeStatus) {
    if (opcao.nome === "CORRIGIDA") {
      return opcao.valor;
    }
  }
  return null;
}

function calcularRiscoProprio(vinculos, valorDeCorrigida) {
  let somaDosCvss = 0;
  for (const vinculo of vinculos) {
    if (vinculo.statusDeTratamento !== valorDeCorrigida) {
      somaDosCvss += vinculo.cvss;
    }
  }
  return Math.round(somaDosCvss * ATIVO_DE_EXEMPLO.fatorDeExposicao * 100) / 100;
}

function criarAcoesDaJanela(pedirFechamento) {
  const botaoDeEditar = criarBotao({
    texto: "Editar",
    variacao: "secundario",
    icone: "editar",
    pequeno: true,
    aoClicar: () => navegarPara(`/ativos/${ATIVO_DE_EXEMPLO.id}/editar`),
  });
  const botaoDeExcluir = criarBotao({
    texto: "Excluir",
    variacao: "secundario",
    icone: "excluir",
    pequeno: true,
  });
  botaoDeExcluir.addEventListener("click", () => {
    abrirBalaoDeExclusao({
      ancora: botaoDeExcluir,
      pergunta: `Excluir ${ATIVO_DE_EXEMPLO.nome}?`,
      explicacao: "Os vínculos e as dependências dele também serão removidos.",
      aoConfirmar: async () => {
        await esperar(500);
        pedirFechamento();
        mostrarAvisoDeSucesso("Ativo excluído");
      },
    });
  });
  return [botaoDeEditar, botaoDeExcluir];
}

function criarNumerosDeRisco(riscoProprio, riscoHerdado) {
  const proprio = criarNumeroDeRisco("Risco próprio", riscoProprio);
  const herdado = criarNumeroDeRisco("Risco herdado", riscoHerdado);
  const efetivo = criarNumeroDeRisco("Risco efetivo", riscoProprio + riscoHerdado);
  const elemento = criarElemento("div", { classe: "numeros-de-risco" }, [
    proprio.elemento,
    herdado.elemento,
    efetivo.elemento,
  ]);

  function animarAte(novoRiscoProprio, novoRiscoHerdado) {
    proprio.numero.animarAte(novoRiscoProprio);
    herdado.numero.animarAte(novoRiscoHerdado);
    efetivo.numero.animarAte(novoRiscoProprio + novoRiscoHerdado);
  }

  return { elemento, animarAte };
}

function criarNumeroDeRisco(rotulo, valorInicial) {
  const numero = criarNumeroAnimado({
    valor: valorInicial,
    formatar: formatarRisco,
    classe: "numero-de-risco-valor",
  });
  const elemento = criarElemento("div", { classe: "numero-de-risco" }, [
    numero.elemento,
    criarElemento("span", { classe: "legenda", texto: rotulo }),
  ]);
  return { elemento, numero };
}

function criarListaDeVinculos(vinculos, opcoesDeStatus, recalcularRiscos) {
  const lista = criarElemento("ul");
  for (const vinculo of vinculos) {
    lista.append(criarLinhaDeVinculo(vinculo, vinculos, opcoesDeStatus, recalcularRiscos));
  }
  return criarElemento("section", {}, [
    criarElemento("h3", {
      classe: "titulo-de-secao lista-de-vinculos-titulo",
      texto: "Vulnerabilidades vinculadas",
    }),
    lista,
  ]);
}

function criarLinhaDeVinculo(vinculo, vinculos, opcoesDeStatus, recalcularRiscos) {
  const pilula = criarPilulaDeStatusTrocavel({
    rotulo: `Status de ${vinculo.nome}`,
    opcoes: opcoesDeStatus,
    valor: vinculo.statusDeTratamento,
    aoMudar: (novoStatus) => {
      vinculo.statusDeTratamento = novoStatus;
      recalcularRiscos();
    },
  });
  const linha = criarElemento("li", { classe: "linha-de-vinculo" });
  const botaoDeDesvincular = criarBotao({
    variacao: "icone",
    icone: "fechar",
    rotuloAcessivel: `Desvincular ${vinculo.nome}`,
    aoClicar: () => {
      vinculos.splice(vinculos.indexOf(vinculo), 1);
      linha.remove();
      recalcularRiscos();
      mostrarAvisoDeSucesso("Vulnerabilidade desvinculada");
    },
  });

  linha.append(
    criarElemento("span", { classe: "linha-de-vinculo-nivel" }, [
      criarElemento("span", { classe: "bolinha", "data-nivel": vinculo.nivel }),
      criarElemento("span", {
        classe: "nome-do-nivel",
        "data-nivel": vinculo.nivel,
        texto: NIVEIS_DE_GRAVIDADE[vinculo.nivel].rotulo,
      }),
    ]),
    criarElemento("span", { classe: "linha-de-vinculo-nome", texto: vinculo.nome }),
    criarElemento("span", {
      classe: "linha-de-vinculo-cvss",
      texto: `CVSS ${formatarCvss(vinculo.cvss)}`,
    }),
    pilula.elemento,
    botaoDeDesvincular,
  );
  return linha;
}

function esperar(milissegundos) {
  return new Promise((resolver) => setTimeout(resolver, milissegundos));
}
