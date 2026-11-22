const LARGURA_VIRTUAL = 1000;
const QUANTIDADE_DE_RODADAS = 300;
const RESFRIAMENTO = 0.97;
const MENOR_TEMPERATURA = 1;
const FORCA_DA_GRAVIDADE = 0.02;
const MENOR_DISTANCIA = 1;
const PROPORCAO_DA_DISTANCIA_IDEAL = 1.2;
const MAIOR_DISTANCIA_IDEAL = 180;
const PROPORCAO_DO_CIRCULO_INICIAL = 0.35;
const ALCANCE_DA_REPULSAO = 2;

export function calcularPosicoesDoMapa(ativos, proporcao) {
  const caixa = { largura: LARGURA_VIRTUAL, altura: LARGURA_VIRTUAL / proporcao };
  const posicoes = criarPosicoesIniciais(ativos, caixa);
  const ligacoes = listarLigacoes(ativos, posicoes);
  const quantidade = Math.max(ativos.length, 1);
  const distanciaIdeal = Math.min(
    Math.sqrt((caixa.largura * caixa.altura) / quantidade) * PROPORCAO_DA_DISTANCIA_IDEAL,
    MAIOR_DISTANCIA_IDEAL,
  );
  let temperatura = caixa.largura / 10;

  for (let rodada = 0; rodada < QUANTIDADE_DE_RODADAS; rodada += 1) {
    const deslocamentos = criarDeslocamentosZerados(posicoes);
    aplicarRepulsao(posicoes, deslocamentos, distanciaIdeal);
    aplicarAtracao(ligacoes, posicoes, deslocamentos, distanciaIdeal);
    aplicarGravidade(posicoes, deslocamentos, caixa);
    moverPosicoes(posicoes, deslocamentos, temperatura, caixa);
    temperatura = Math.max(temperatura * RESFRIAMENTO, MENOR_TEMPERATURA);
  }

  return transformarEmFracoes(posicoes, caixa);
}

function criarPosicoesIniciais(ativos, caixa) {
  const ativosEmOrdem = [...ativos];
  ativosEmOrdem.sort((primeiro, segundo) => primeiro.id - segundo.id);
  const raio = Math.min(caixa.largura, caixa.altura) * PROPORCAO_DO_CIRCULO_INICIAL;
  const posicoes = new Map();
  for (const [indice, ativo] of ativosEmOrdem.entries()) {
    if (ativosEmOrdem.length === 1) {
      posicoes.set(ativo.id, { x: caixa.largura / 2, y: caixa.altura / 2 });
      continue;
    }
    const angulo = -Math.PI / 2 + (2 * Math.PI * indice) / ativosEmOrdem.length;
    posicoes.set(ativo.id, {
      x: caixa.largura / 2 + raio * Math.cos(angulo),
      y: caixa.altura / 2 + raio * Math.sin(angulo),
    });
  }
  return posicoes;
}

function listarLigacoes(ativos, posicoes) {
  const ligacoes = [];
  for (const ativo of ativos) {
    for (const dependencia of ativo.dependencias) {
      if (posicoes.has(dependencia.id_ativo_do_qual_depende)) {
        ligacoes.push({ origem: ativo.id, destino: dependencia.id_ativo_do_qual_depende });
      }
    }
  }
  return ligacoes;
}

function criarDeslocamentosZerados(posicoes) {
  const deslocamentos = new Map();
  for (const id of posicoes.keys()) {
    deslocamentos.set(id, { x: 0, y: 0 });
  }
  return deslocamentos;
}

function aplicarRepulsao(posicoes, deslocamentos, distanciaIdeal) {
  const identificadores = [...posicoes.keys()];
  for (let primeiro = 0; primeiro < identificadores.length; primeiro += 1) {
    for (let segundo = primeiro + 1; segundo < identificadores.length; segundo += 1) {
      const idPrimeiro = identificadores[primeiro];
      const idSegundo = identificadores[segundo];
      const diferenca = medirDiferenca(posicoes.get(idPrimeiro), posicoes.get(idSegundo));
      if (diferenca.distancia > distanciaIdeal * ALCANCE_DA_REPULSAO) {
        continue;
      }
      const forca = (distanciaIdeal * distanciaIdeal) / diferenca.distancia;
      empurrar(deslocamentos.get(idPrimeiro), diferenca, forca);
      empurrar(deslocamentos.get(idSegundo), diferenca, -forca);
    }
  }
}

function aplicarAtracao(ligacoes, posicoes, deslocamentos, distanciaIdeal) {
  for (const ligacao of ligacoes) {
    const diferenca = medirDiferenca(posicoes.get(ligacao.origem), posicoes.get(ligacao.destino));
    const forca = (diferenca.distancia * diferenca.distancia) / distanciaIdeal;
    empurrar(deslocamentos.get(ligacao.origem), diferenca, -forca);
    empurrar(deslocamentos.get(ligacao.destino), diferenca, forca);
  }
}

function aplicarGravidade(posicoes, deslocamentos, caixa) {
  for (const [id, posicao] of posicoes) {
    const deslocamento = deslocamentos.get(id);
    deslocamento.x +=
      ((caixa.largura / 2 - posicao.x) * FORCA_DA_GRAVIDADE * caixa.altura) / caixa.largura;
    deslocamento.y += (caixa.altura / 2 - posicao.y) * FORCA_DA_GRAVIDADE;
  }
}

function moverPosicoes(posicoes, deslocamentos, temperatura, caixa) {
  for (const [id, posicao] of posicoes) {
    const deslocamento = deslocamentos.get(id);
    const tamanho = Math.max(Math.hypot(deslocamento.x, deslocamento.y), MENOR_DISTANCIA);
    const passo = Math.min(tamanho, temperatura);
    posicao.x = limitar(posicao.x + (deslocamento.x / tamanho) * passo, 0, caixa.largura);
    posicao.y = limitar(posicao.y + (deslocamento.y / tamanho) * passo, 0, caixa.altura);
  }
}

function medirDiferenca(origem, destino) {
  const x = origem.x - destino.x;
  const y = origem.y - destino.y;
  return { x, y, distancia: Math.max(Math.hypot(x, y), MENOR_DISTANCIA) };
}

function empurrar(deslocamento, diferenca, forca) {
  deslocamento.x += (diferenca.x / diferenca.distancia) * forca;
  deslocamento.y += (diferenca.y / diferenca.distancia) * forca;
}

function limitar(valor, minimo, maximo) {
  return Math.min(Math.max(valor, minimo), maximo);
}

function transformarEmFracoes(posicoes, caixa) {
  const limites = medirLimites(posicoes);
  const centroX = (limites.menorX + limites.maiorX) / 2;
  const centroY = (limites.menorY + limites.maiorY) / 2;
  const fracoes = new Map();
  for (const [id, posicao] of posicoes) {
    fracoes.set(id, {
      x: 0.5 + (posicao.x - centroX) / caixa.largura,
      y: 0.5 + (posicao.y - centroY) / caixa.altura,
    });
  }
  return fracoes;
}

function medirLimites(posicoes) {
  const limites = { menorX: Infinity, maiorX: -Infinity, menorY: Infinity, maiorY: -Infinity };
  for (const posicao of posicoes.values()) {
    limites.menorX = Math.min(limites.menorX, posicao.x);
    limites.maiorX = Math.max(limites.maiorX, posicao.x);
    limites.menorY = Math.min(limites.menorY, posicao.y);
    limites.maiorY = Math.max(limites.maiorY, posicao.y);
  }
  return limites;
}
