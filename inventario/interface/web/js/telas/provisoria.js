import { criarElemento } from "../elementos.js";

export function criarTelaProvisoria(titulo, etapa) {
  return function montarTelaProvisoria(tela) {
    tela.append(
      criarElemento("section", { classe: "tela-provisoria" }, [
        criarElemento("h1", { classe: "titulo-de-tela", texto: titulo }),
        criarElemento("p", {
          classe: "texto-de-apoio",
          texto: `Esta tela chega na Etapa ${etapa} do frontend.`,
        }),
        criarElemento("a", {
          classe: "botao botao-secundario",
          href: "#/componentes",
          texto: "Ver os componentes",
        }),
      ]),
    );
  };
}

export function montarTelaNaoEncontrada(tela) {
  tela.append(
    criarElemento("section", { classe: "tela-provisoria" }, [
      criarElemento("h1", { classe: "titulo-de-tela", texto: "Página não encontrada" }),
      criarElemento("p", {
        classe: "texto-de-apoio",
        texto: "Este endereço não corresponde a nenhuma tela do sistema.",
      }),
      criarElemento("a", {
        classe: "botao botao-principal",
        href: "#/",
        texto: "Ir para o início",
      }),
    ]),
  );
}
