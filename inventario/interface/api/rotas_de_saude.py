from flask import Blueprint


def criar_rotas_de_saude():
    rotas = Blueprint("saude", __name__)

    @rotas.get("/saude")
    def verificar_saude():
        return {"status": "ok"}

    return rotas
