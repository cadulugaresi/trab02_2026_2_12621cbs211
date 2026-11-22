from pathlib import Path

from flask import Blueprint, send_from_directory

PASTA_DO_FRONTEND = Path(__file__).resolve().parent.parent / "web"


def criar_rotas_do_frontend():
    rotas = Blueprint("frontend", __name__)

    @rotas.get("/")
    def abrir_pagina_do_frontend():
        return send_from_directory(PASTA_DO_FRONTEND, "index.html")

    @rotas.get("/web/<path:caminho_do_arquivo>")
    def entregar_arquivo_do_frontend(caminho_do_arquivo):
        return send_from_directory(PASTA_DO_FRONTEND, caminho_do_arquivo)

    return rotas
