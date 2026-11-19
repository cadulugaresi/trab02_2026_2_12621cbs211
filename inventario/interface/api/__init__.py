from flask import Flask
from werkzeug.exceptions import HTTPException

from inventario.dominio.excecoes import (
    DadoInvalidoError,
    PersistenciaError,
    RecursoNaoEncontradoError,
)
from inventario.interface.api.rotas_de_ativos import criar_rotas_de_ativos
from inventario.interface.api.rotas_de_dependencias import criar_rotas_de_dependencias
from inventario.interface.api.rotas_de_opcoes import criar_rotas_de_opcoes
from inventario.interface.api.rotas_de_riscos import criar_rotas_de_riscos
from inventario.interface.api.rotas_de_saude import criar_rotas_de_saude
from inventario.interface.api.rotas_de_vinculos import criar_rotas_de_vinculos
from inventario.interface.api.rotas_de_vulnerabilidades import criar_rotas_de_vulnerabilidades

MENSAGENS_DOS_ERROS_HTTP = {
    404: "Rota não encontrada.",
    405: "Método não permitido para esta rota.",
    500: "Erro interno do servidor.",
}


def criar_app(repositorio, ativos, catalogo):
    app = Flask(__name__)

    @app.errorhandler(DadoInvalidoError)
    def responder_dado_invalido(erro):
        return {"erro": str(erro)}, 400

    @app.errorhandler(RecursoNaoEncontradoError)
    def responder_recurso_nao_encontrado(erro):
        return {"erro": str(erro)}, 404

    @app.errorhandler(PersistenciaError)
    def responder_erro_de_persistencia(erro):
        return {"erro": str(erro)}, 500

    @app.errorhandler(HTTPException)
    def responder_erro_http(erro):
        mensagem = MENSAGENS_DOS_ERROS_HTTP.get(erro.code, erro.name)
        return {"erro": mensagem}, erro.code

    app.register_blueprint(criar_rotas_de_saude())
    app.register_blueprint(criar_rotas_de_opcoes())
    app.register_blueprint(criar_rotas_de_ativos(repositorio, ativos))
    app.register_blueprint(criar_rotas_de_vulnerabilidades(repositorio, ativos, catalogo))
    app.register_blueprint(criar_rotas_de_vinculos(repositorio, ativos, catalogo))
    app.register_blueprint(criar_rotas_de_dependencias(repositorio, ativos))
    app.register_blueprint(criar_rotas_de_riscos(ativos, catalogo))

    return app
