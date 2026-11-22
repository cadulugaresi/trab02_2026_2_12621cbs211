import { ativoPassaNosFiltros, nomeCombinaComABusca } from "../ativos/filtros-de-ativos.js";

export function escolherAtivosVisiveis(ativos, filtros) {
  const filtrados = [];
  for (const ativo of ativos) {
    if (ativoPassaNosFiltros(ativo, filtros)) {
      filtrados.push(ativo);
    }
  }
  if (filtros.nome.trim() === "") {
    return { ativos: filtrados, buscados: new Set() };
  }

  const buscados = new Set();
  for (const ativo of filtrados) {
    if (nomeCombinaComABusca(ativo.nome, filtros.nome)) {
      buscados.add(ativo.id);
    }
  }

  const idsVisiveis = new Set(buscados);
  for (const ativo of ativos) {
    for (const dependencia of ativo.dependencias) {
      if (buscados.has(ativo.id)) {
        idsVisiveis.add(dependencia.id_ativo_do_qual_depende);
      }
      if (buscados.has(dependencia.id_ativo_do_qual_depende)) {
        idsVisiveis.add(ativo.id);
      }
    }
  }

  const visiveis = [];
  for (const ativo of ativos) {
    if (idsVisiveis.has(ativo.id)) {
      visiveis.push(ativo);
    }
  }
  return { ativos: visiveis, buscados };
}

export function contarLigacoesVisiveis(ativos, buscados) {
  const idsVisiveis = new Set();
  for (const ativo of ativos) {
    idsVisiveis.add(ativo.id);
  }
  let quantidade = 0;
  for (const ativo of ativos) {
    for (const dependencia of ativo.dependencias) {
      const idDestino = dependencia.id_ativo_do_qual_depende;
      if (idsVisiveis.has(idDestino) && ligacaoAparece(ativo.id, idDestino, buscados)) {
        quantidade += 1;
      }
    }
  }
  return quantidade;
}

export function ligacaoAparece(idOrigem, idDestino, buscados) {
  if (buscados.size === 0) {
    return true;
  }
  return buscados.has(idOrigem) || buscados.has(idDestino);
}
