let contadorDeIdentificadores = 0;

export function criarElemento(etiqueta, propriedades = {}, filhos = []) {
  const elemento = document.createElement(etiqueta);
  aplicarPropriedades(elemento, propriedades);
  adicionarFilhos(elemento, filhos);
  return elemento;
}

export function adicionarFilhos(elemento, filhos) {
  for (const filho of filhos) {
    if (filho === null || filho === undefined || filho === false) {
      continue;
    }
    elemento.append(filho);
  }
}

export function gerarIdentificador(prefixo) {
  contadorDeIdentificadores += 1;
  return `${prefixo}-${contadorDeIdentificadores}`;
}

function aplicarPropriedades(elemento, propriedades) {
  for (const [nome, valor] of Object.entries(propriedades)) {
    if (valor === null || valor === undefined || valor === false) {
      continue;
    }
    if (nome === "classe") {
      elemento.className = valor;
    } else if (nome === "texto") {
      elemento.textContent = valor;
    } else if (valor === true) {
      elemento.setAttribute(nome, "");
    } else {
      elemento.setAttribute(nome, valor);
    }
  }
}
