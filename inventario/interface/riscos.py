from inventario.dominio.excecoes import DadoInvalidoError
from inventario.servicos.riscos import AnaliseDeRisco


def analisar_risco(ativos, catalogo):
    if len(ativos) == 0:
        print("Não há ativos cadastrados para analisar.")
    else:
        try:
            analise = AnaliseDeRisco(ativos, catalogo)
            print("\n=== Análise de risco ===\n")
            for posicao, id_ativo in enumerate(analise.ranking(), start=1):
                ativo = ativos[id_ativo]
                print(
                    f"{posicao}º {ativo.nome} ({type(ativo).__name__}) "
                    f"| fator: {ativo.fator_exposicao} "
                    f"| próprio: {analise.risco_proprio_do_ativo(id_ativo):.2f} "
                    f"| herdado: {analise.risco_herdado_do_ativo(id_ativo):.2f} "
                    f"| efetivo: {analise.risco_efetivo_do_ativo(id_ativo):.2f}"
                )
            print("\n=== Legenda ===\n")
            print(
                "Fator:   peso do tipo do ativo; quanto maior, mais exposto\n"
                "Próprio: fator × soma dos CVSS das vulnerabilidades não corrigidas\n"
                "Herdado: fração × risco efetivo de cada ativo do qual ele depende\n"
                "Efetivo: próprio + herdado; é o que ordena o ranking"
            )

        except DadoInvalidoError as erro:
            print(erro)
