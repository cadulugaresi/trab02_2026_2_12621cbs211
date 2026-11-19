def valor_enviado_ou_atual(corpo, campo, valor_atual):
    if corpo.get(campo) is None:
        return valor_atual
    return corpo[campo]
