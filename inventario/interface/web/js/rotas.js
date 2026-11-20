import {
  montarTelaDeEditarAtivo,
  montarTelaDeNovoAtivo,
} from "./telas/ativos/formulario-de-ativo.js";
import { abrirJanelaDoAtivo } from "./telas/ativos/janela-do-ativo.js";
import { montarTelaDeAtivos } from "./telas/ativos/lista-de-ativos.js";
import { montarTelaDeComponentes } from "./telas/componentes.js";
import { abrirJanelaDeExemplo } from "./telas/janela-de-exemplo.js";
import { criarTelaProvisoria, montarTelaNaoEncontrada } from "./telas/provisoria.js";
import { montarTelaDeVinculos } from "./telas/vinculos/tela-de-vinculos.js";
import {
  montarTelaDeEditarVulnerabilidade,
  montarTelaDeNovaVulnerabilidade,
} from "./telas/vulnerabilidades/formulario-de-vulnerabilidade.js";
import { abrirJanelaDaVulnerabilidade } from "./telas/vulnerabilidades/janela-da-vulnerabilidade.js";
import { montarTelaDeVulnerabilidades } from "./telas/vulnerabilidades/lista-de-vulnerabilidades.js";

export const ROTAS = [
  {
    caminho: "/",
    titulo: "Início",
    serveDeFundo: true,
    montar: criarTelaProvisoria("Início", 4),
  },
  { caminho: "/ativos", titulo: "Ativos", serveDeFundo: true, montar: montarTelaDeAtivos },
  {
    caminho: "/ativos/mapa",
    titulo: "Mapa",
    serveDeFundo: true,
    montar: criarTelaProvisoria("Mapa dos ativos", 4),
  },
  {
    caminho: "/ativos/novo",
    titulo: "Novo ativo",
    escondeCadastrar: true,
    montar: montarTelaDeNovoAtivo,
  },
  { caminho: "/ativos/:id", fundo: "/ativos", janela: abrirJanelaDoAtivo },
  {
    caminho: "/ativos/:id/editar",
    titulo: "Editar ativo",
    escondeCadastrar: true,
    montar: montarTelaDeEditarAtivo,
  },
  {
    caminho: "/vulnerabilidades",
    titulo: "Vulnerabilidades",
    serveDeFundo: true,
    montar: montarTelaDeVulnerabilidades,
  },
  {
    caminho: "/vulnerabilidades/novo",
    titulo: "Nova vulnerabilidade",
    escondeCadastrar: true,
    montar: montarTelaDeNovaVulnerabilidade,
  },
  {
    caminho: "/vulnerabilidades/:id",
    fundo: "/vulnerabilidades",
    janela: abrirJanelaDaVulnerabilidade,
  },
  {
    caminho: "/vulnerabilidades/:id/editar",
    titulo: "Editar vulnerabilidade",
    escondeCadastrar: true,
    montar: montarTelaDeEditarVulnerabilidade,
  },
  {
    caminho: "/vinculos",
    titulo: "Vínculos",
    serveDeFundo: true,
    montar: montarTelaDeVinculos,
  },
  {
    caminho: "/ranking",
    titulo: "Ranking",
    serveDeFundo: true,
    montar: criarTelaProvisoria("Ranking de riscos", 4),
  },
  {
    caminho: "/componentes",
    titulo: "Componentes",
    serveDeFundo: true,
    montar: montarTelaDeComponentes,
  },
  { caminho: "/componentes/janela", fundo: "/componentes", janela: abrirJanelaDeExemplo },
];

export const ROTA_NAO_ENCONTRADA = {
  titulo: "Página não encontrada",
  montar: montarTelaNaoEncontrada,
};
