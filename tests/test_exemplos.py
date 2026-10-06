import pytest
from funcoes_t2 import *

def test_validar_status_1_retorna_ativo():
    resultado = validar_status("1")
    assert resultado == StatusDoAtivo.ATIVO

def test_validar_status_invalido_levanta_erro():
    with pytest.raises(DadoInvalidoError):
        validar_status("99")

@pytest.mark.parametrize("entrada, esperado", [
    ("1", Setor.TI),
    ("2", Setor.FINANCEIRO),
    ("3", Setor.MARKETING),
    ("4", Setor.RH),
    ("5", Setor.JURIDICO),
])
def test_validar_setor_parametrizado(entrada, esperado):
    assert validar_setor(entrada) == esperado