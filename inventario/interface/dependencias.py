from inventario.servicos.dependencias import somar_fracoes


def mostrar_dependencias(ativo, ativos):
    if not ativo.dependencias:
        print("Este ativo não depende de nenhum outro ativo.")
        return

    for id_ativo_do_qual_depende, fracao in ativo.dependencias.items():
        ativo_do_qual_depende = ativos[id_ativo_do_qual_depende]
        print(f"""
    ID: {id_ativo_do_qual_depende}
    Ativo: {ativo_do_qual_depende.nome}
    Tipo: {type(ativo_do_qual_depende).__name__}
    Fração herdada: {fracao}""")

    soma = somar_fracoes(ativo.dependencias)
    print(f"""
    Soma das frações: {soma}. Ainda cabem {round(1 - soma, 6)}.""")
