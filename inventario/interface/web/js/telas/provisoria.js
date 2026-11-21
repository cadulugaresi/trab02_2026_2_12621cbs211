import { criarElemento } from "../elementos.js";

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
