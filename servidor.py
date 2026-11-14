from flask import Flask
from inventario.persistencia.banco_sqlite import RepositorioSQLite
from inventario.dominio.excecoes import PersistenciaError

app = Flask(__name__)

try:
    repositorio = RepositorioSQLite()
    ativos = repositorio.carregar_ativos()
    catalogo = repositorio.carregar_catalogo()

except PersistenciaError as erro:
    print(erro)
    raise SystemExit(
        "Erro de Persistência: Não foi possível carregar os dados do banco de dados. O servidor não foi iniciado."
    )


@app.get("/saude")
def verificar_saude():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
