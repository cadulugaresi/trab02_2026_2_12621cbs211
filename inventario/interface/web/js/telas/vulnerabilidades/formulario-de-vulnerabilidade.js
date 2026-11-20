import {
  buscarVulnerabilidade,
  cadastrarVulnerabilidade,
  editarVulnerabilidade,
} from "../../api.js";
import { mostrarAvisoDeSucesso } from "../../componentes/aviso-de-sucesso.js";
import { liberarBotao, marcarBotaoComoOcupado } from "../../componentes/botoes.js";
import {
  AJUDA_DO_CVSS,
  EXPLICACAO_DO_CVSS,
  criarCampoDeCvss,
} from "../../componentes/campo-de-cvss.js";
import { criarCampoDeTexto, criarLinhaComValidacao } from "../../componentes/campos.js";
import { criarElemento } from "../../elementos.js";
import { trocarEnderecoPor } from "../../roteador.js";
import { validarCvssPreenchido, validarTextoObrigatorio } from "../../validacoes.js";
import {
  criarEstruturaDoFormulario,
  criarGrupoDoFormulario,
  mostrarErrosNasLinhas,
} from "../estrutura-do-formulario.js";

export function montarTelaDeNovaVulnerabilidade(tela) {
  montarFormularioDeVulnerabilidade(tela, null);
}

export function montarTelaDeEditarVulnerabilidade(tela, { parametros }) {
  montarFormularioDeVulnerabilidade(tela, parametros.id);
}

function montarFormularioDeVulnerabilidade(tela, idEmEdicao) {
  const ehEdicao = idEmEdicao !== null;
  const estrutura = criarEstruturaDoFormulario({
    titulo: ehEdicao ? "Editar vulnerabilidade" : "Nova vulnerabilidade",
    textoDoBotao: "Salvar vulnerabilidade",
    enderecoDeVolta: ehEdicao ? `/vulnerabilidades/${idEmEdicao}` : "/vulnerabilidades",
  });
  tela.append(estrutura.formulario);

  const buscarDados = ehEdicao ? buscarVulnerabilidade(idEmEdicao) : Promise.resolve(null);
  buscarDados
    .then((vulnerabilidade) => {
      const campos = criarCampos(vulnerabilidade);
      estrutura.areaDosCampos.append(campos.elemento);
      estrutura.subtitulo.textContent = ehEdicao
        ? `ID ${vulnerabilidade.id_vulnerabilidade} · ${vulnerabilidade.nome_vulnerabilidade}`
        : "O ID é criado pelo sistema ao salvar";
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
    mostrarErrosNasLinhas(erros, campos.linhas);
    return;
  }

  const { nome, cvss } = campos.obterValores();
  marcarBotaoComoOcupado(estrutura.botaoDeSalvar, "Salvando…");
  try {
    const vulnerabilidadeSalva =
      idEmEdicao === null
        ? await cadastrarVulnerabilidade(nome, cvss)
        : await editarVulnerabilidade(idEmEdicao, { nome_vulnerabilidade: nome, cvss: cvss });
    mostrarAvisoDeSucesso(
      idEmEdicao === null ? "Vulnerabilidade cadastrada" : "Vulnerabilidade atualizada",
    );
    trocarEnderecoPor(`/vulnerabilidades/${vulnerabilidadeSalva.id_vulnerabilidade}`);
  } catch (erro) {
    liberarBotao(estrutura.botaoDeSalvar);
    estrutura.faixa.mostrar(erro.message);
  }
}

function criarCampos(vulnerabilidade) {
  const nome = criarCampoDeTexto({
    nome: "nome_vulnerabilidade",
    valor: vulnerabilidade ? vulnerabilidade.nome_vulnerabilidade : "",
    textoDeExemplo: "Ex.: Log4Shell",
    tamanhoMaximo: 120,
  });
  const cvss = criarCampoDeCvss({ valor: vulnerabilidade ? vulnerabilidade.cvss : null });
  const linhas = {
    nome: criarLinhaComValidacao({
      rotulo: "Nome",
      controle: nome,
      ajuda: "Como a vulnerabilidade aparece nas listas",
    }),
    cvss: criarLinhaComValidacao({
      rotulo: "CVSS",
      controle: cvss.elemento,
      alvoDoRotulo: cvss.campo,
      ajuda: AJUDA_DO_CVSS,
      explicacaoDoConceito: EXPLICACAO_DO_CVSS,
    }),
  };
  cvss.ligarTextoDeAjuda(linhas.cvss.textoDeAjuda);

  const elemento = criarElemento("div", {}, [
    criarGrupoDoFormulario("Identificação", [linhas.nome.elemento]),
    criarGrupoDoFormulario("Gravidade", [linhas.cvss.elemento]),
  ]);

  function validar() {
    const erros = [];
    validarTextoObrigatorio(erros, "nome", nome.value);
    validarCvssPreenchido(erros, "cvss", cvss.obterValor());
    return erros;
  }

  function limparErros() {
    for (const linha of Object.values(linhas)) {
      linha.limparErro();
    }
  }

  function obterValores() {
    return { nome: nome.value.trim(), cvss: cvss.obterValor() };
  }

  return { elemento, linhas, validar, limparErros, obterValores };
}
