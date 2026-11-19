from flask import Flask

from inventario.dominio.excecoes import PersistenciaError
from inventario.interface.api.rotas_de_ativos import criar_rotas_de_ativos
from inventario.interface.api.rotas_de_riscos import criar_rotas_de_riscos
from inventario.interface.api.rotas_de_saude import criar_rotas_de_saude
from inventario.interface.api.rotas_de_vinculos import criar_rotas_de_vinculos
from inventario.interface.api.rotas_de_vulnerabilidades import criar_rotas_de_vulnerabilidades


def criar_app(repositorio, ativos, catalogo):
    app = Flask(__name__)

    @app.errorhandler(PersistenciaError)
    def responder_erro_de_persistencia(erro):
        return {"erro": str(erro)}, 500

    app.register_blueprint(criar_rotas_de_saude())
    app.register_blueprint(criar_rotas_de_ativos(repositorio, ativos))
    app.register_blueprint(criar_rotas_de_vulnerabilidades(repositorio, catalogo))
    app.register_blueprint(criar_rotas_de_vinculos(repositorio, ativos, catalogo))
    app.register_blueprint(criar_rotas_de_riscos(ativos, catalogo))

    return app
