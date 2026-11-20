import { mostrarAvisoDeSucesso } from "../componentes/aviso-de-sucesso.js";
import { abrirBalaoDeExclusao } from "../componentes/balao-de-exclusao.js";
import { criarBotao } from "../componentes/botoes.js";
import { criarFaixaDeErro } from "../componentes/faixa-de-erro.js";
import { abrirJanela } from "../componentes/janela.js";
import { criarLinhaDeVinculo } from "../componentes/linha-de-vinculo.js";
import { criarNumerosDeRisco } from "../componentes/numeros-de-risco.js";
import { criarElemento } from "../elementos.js";
import { carregarOpcoes } from "../opcoes.js";
import { navegarPara } from "../roteador.js";

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
  const riscos = criarNumerosDeRisco(calcularRiscos(vinculos, null));
  const faixa = criarFaixaDeErro();
  const corpo = criarElemento("div", {}, [faixa.elemento, riscos.elemento]);

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
      const recalcularRiscos = () => riscos.animarAte(calcularRiscos(vinculos, valorDeCorrigida));
      corpo.append(criarListaDeVinculos(vinculos, opcoes.statusDeTratamento, recalcularRiscos));
    })
    .catch((erro) => faixa.mostrar(erro.message));
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

function calcularRiscos(vinculos, valorDeCorrigida) {
  let somaDosCvss = 0;
  for (const vinculo of vinculos) {
    if (vinculo.statusDeTratamento !== valorDeCorrigida) {
      somaDosCvss += vinculo.cvss;
    }
  }
  const proprio = Math.round(somaDosCvss * ATIVO_DE_EXEMPLO.fatorDeExposicao * 100) / 100;
  const herdado = ATIVO_DE_EXEMPLO.riscoHerdado;
  return { proprio, herdado, efetivo: proprio + herdado };
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

function criarListaDeVinculos(vinculos, opcoesDeStatus, recalcularRiscos) {
  const lista = criarElemento("ul");
  for (const vinculo of vinculos) {
    lista.append(
      criarLinhaDeVinculo({
        nome: vinculo.nome,
        cvss: vinculo.cvss,
        nivel: vinculo.nivel,
        opcoesDeStatus: opcoesDeStatus,
        statusDeTratamento: vinculo.statusDeTratamento,
        aoMudarStatus: (novoStatus) => {
          vinculo.statusDeTratamento = novoStatus;
          recalcularRiscos();
        },
        aoDesvincular: () => {
          vinculos.splice(vinculos.indexOf(vinculo), 1);
          recalcularRiscos();
          mostrarAvisoDeSucesso("Vulnerabilidade desvinculada");
        },
        aoFalhar: () => {},
      }),
    );
  }
  return criarElemento("section", { classe: "secao-da-janela" }, [
    criarElemento("h3", {
      classe: "titulo-de-secao secao-da-janela-titulo",
      texto: "Vulnerabilidades vinculadas",
    }),
    lista,
  ]);
}

function esperar(milissegundos) {
  return new Promise((resolver) => setTimeout(resolver, milissegundos));
}
