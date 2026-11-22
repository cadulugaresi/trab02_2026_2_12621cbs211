import {
  montarTelaDeEditarAtivo,
  montarTelaDeNovoAtivo,
} from "./telas/ativos/formulario-de-ativo.js";
import { abrirJanelaDoAtivo } from "./telas/ativos/janela-do-ativo.js";
import { montarTelaDeAtivos } from "./telas/ativos/lista-de-ativos.js";
import { montarTelaDeInicio } from "./telas/inicio/tela-de-inicio.js";
import { montarTelaDoMapa } from "./telas/mapa/tela-do-mapa.js";
import { montarTelaNaoEncontrada } from "./telas/tela-nao-encontrada.js";
import { montarTelaDeRanking } from "./telas/ranking/tela-de-ranking.js";
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
    montar: montarTelaDeInicio,
  },
  { caminho: "/ativos", titulo: "Ativos", serveDeFundo: true, montar: montarTelaDeAtivos },
  {
    caminho: "/ativos/mapa",
    titulo: "Mapa",
    serveDeFundo: true,
    montar: montarTelaDoMapa,
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
    montar: montarTelaDeRanking,
  },
];

export const ROTA_NAO_ENCONTRADA = {
  titulo: "Página não encontrada",
  montar: montarTelaNaoEncontrada,
};
