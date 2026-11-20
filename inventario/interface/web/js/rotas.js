import { montarTelaDeComponentes } from "./telas/componentes.js";
import { abrirJanelaDeExemplo } from "./telas/janela-de-exemplo.js";
import { criarTelaProvisoria, montarTelaNaoEncontrada } from "./telas/provisoria.js";

export const ROTAS = [
  { caminho: "/", titulo: "Início", montar: criarTelaProvisoria("Início", 4) },
  { caminho: "/ativos", titulo: "Ativos", montar: criarTelaProvisoria("Ativos", 2) },
  { caminho: "/ativos/mapa", titulo: "Mapa", montar: criarTelaProvisoria("Mapa dos ativos", 4) },
  { caminho: "/ativos/novo", titulo: "Novo ativo", montar: criarTelaProvisoria("Novo ativo", 2) },
  {
    caminho: "/ativos/:id",
    titulo: "Ativo",
    montar: criarTelaProvisoria("Detalhes do ativo", 2),
  },
  {
    caminho: "/ativos/:id/editar",
    titulo: "Editar ativo",
    montar: criarTelaProvisoria("Editar ativo", 2),
  },
  {
    caminho: "/vulnerabilidades",
    titulo: "Vulnerabilidades",
    montar: criarTelaProvisoria("Vulnerabilidades", 3),
  },
  {
    caminho: "/vulnerabilidades/novo",
    titulo: "Nova vulnerabilidade",
    montar: criarTelaProvisoria("Nova vulnerabilidade", 3),
  },
  {
    caminho: "/vulnerabilidades/:id",
    titulo: "Vulnerabilidade",
    montar: criarTelaProvisoria("Detalhes da vulnerabilidade", 3),
  },
  {
    caminho: "/vulnerabilidades/:id/editar",
    titulo: "Editar vulnerabilidade",
    montar: criarTelaProvisoria("Editar vulnerabilidade", 3),
  },
  { caminho: "/vinculos", titulo: "Vínculos", montar: criarTelaProvisoria("Vínculos", 3) },
  { caminho: "/ranking", titulo: "Ranking", montar: criarTelaProvisoria("Ranking de riscos", 4) },
  { caminho: "/componentes", titulo: "Componentes", montar: montarTelaDeComponentes },
  { caminho: "/componentes/janela", fundo: "/componentes", janela: abrirJanelaDeExemplo },
];

export const ROTA_NAO_ENCONTRADA = {
  titulo: "Página não encontrada",
  montar: montarTelaNaoEncontrada,
};
