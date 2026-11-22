import { criarElemento } from "../elementos.js";
import { criarIcone } from "../icones.js";

export function criarFaixaDeErro() {
  const texto = criarElemento("p", { classe: "faixa-de-erro-texto" });
  const elemento = criarElemento(
    "div",
    { classe: "faixa-de-erro", role: "alert", hidden: true },
    [criarIcone("alerta"), texto],
  );

  function mostrar(mensagem) {
    texto.textContent = mensagem;
    elemento.hidden = false;
    elemento.scrollIntoView({ block: "nearest" });
  }

  function esconder() {
    elemento.hidden = true;
    texto.textContent = "";
  }

  return { elemento, mostrar, esconder };
}
