def vulnerabilidade_para_resposta(vulnerabilidade):
    resposta = vulnerabilidade.para_dicionario()
    resposta["nivel"] = vulnerabilidade.nivel().name
    return resposta
