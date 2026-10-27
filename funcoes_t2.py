import json
from enum import Enum

ARQUIVO_DADOS = "ativos.json"
ARQUIVO_CATALOGO = "vulnerabilidades.json"


class Vulnerabilidade:
    def __init__(self, id_vulnerabilidade, nome_vulnerabilidade, cvss):
        self.id_vulnerabilidade = id_vulnerabilidade
        self.nome_vulnerabilidade = nome_vulnerabilidade
        self.cvss = cvss

    def nivel(self):
        if self.cvss > 8.9:
            return NivelDaVulnerabilidade.CRITICO
        elif self.cvss > 6.9:
            return NivelDaVulnerabilidade.ALTO
        elif self.cvss > 3.9:
            return NivelDaVulnerabilidade.MEDIO
        else:
            return NivelDaVulnerabilidade.BAIXO

    def para_dicionario(self):
        return {
            "id_vulnerabilidade": self.id_vulnerabilidade,
            "nome_vulnerabilidade": self.nome_vulnerabilidade,
            "cvss": self.cvss,
        }

    @classmethod
    def de_dicionario(cls, dicionario_vulnerabilidade):
        return cls(
            dicionario_vulnerabilidade["id_vulnerabilidade"],
            dicionario_vulnerabilidade["nome_vulnerabilidade"],
            dicionario_vulnerabilidade["cvss"],
        )


class Ativo:

    def __init__(self, id, nome, setor, responsavel, status):
        self.id = id
        self.nome = nome
        self.setor = setor
        self.responsavel = responsavel
        self.status = status
        self.vulnerabilidades = {}

    def exibir_detalhes(self):
        return f"""
            ID: {self.id}
            Nome: {self.nome}
            Tipo: {type(self).__name__}
            Setor: {self.setor.name}
            Responsável: {self.responsavel}
            Status: {self.status.name}
            """

    def para_dicionario(self):
        lista_de_vulns = []

        for id_vulnerabilidade, status in self.vulnerabilidades.items():
            lista_de_vulns.append(
                {"id_vulnerabilidade": id_vulnerabilidade, "status_tratamento": status.value}
            )

        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": type(self).__name__,
            "setor": self.setor.value,
            "responsavel": self.responsavel,
            "status": self.status.value,
            "vulnerabilidades": lista_de_vulns,
        }


class Notebook(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, sistema_operacional, tela):
        super().__init__(id, nome, setor, responsavel, status)
        self.sistema_operacional = sistema_operacional
        self.tela = tela

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Sistema operacional: {self.sistema_operacional}
            Tamanho da tela: {self.tela} polegadas
            """

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["sistema_operacional"] = self.sistema_operacional
        dicionario_base["tela"] = self.tela
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            dicionario_do_ativo["sistema_operacional"],
            dicionario_do_ativo["tela"],
        )


class Roteador(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, portas, velocidade):
        super().__init__(id, nome, setor, responsavel, status)
        self.portas = portas
        self.velocidade = velocidade

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Qtde de portas: {self.portas}
            Velocidade: {self.velocidade}MB
            """

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["portas"] = self.portas
        dicionario_base["velocidade"] = self.velocidade
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            dicionario_do_ativo["portas"],
            dicionario_do_ativo["velocidade"],
        )


class Servidor(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, ram, armazenamento):
        super().__init__(id, nome, setor, responsavel, status)
        self.ram = ram
        self.armazenamento = armazenamento

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Memória RAM: {self.ram}GB
            Qtde armazenamento: {self.armazenamento}T
            """

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["ram"] = self.ram
        dicionario_base["armazenamento"] = self.armazenamento
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            dicionario_do_ativo["ram"],
            dicionario_do_ativo["armazenamento"],
        )


class Impressora(Ativo):
    def __init__(self, id, nome, setor, responsavel, status, cor, tecnologia):
        super().__init__(id, nome, setor, responsavel, status)
        self.cor = cor
        self.tecnologia = tecnologia

    def exibir_detalhes(self):
        detalhes_base = super().exibir_detalhes()
        return f"""
            {detalhes_base}
            Cor: {self.cor.name}
            Tecnologia: {self.tecnologia.name}
            """

    def para_dicionario(self):
        dicionario_base = super().para_dicionario()
        dicionario_base["cor"] = self.cor.value
        dicionario_base["tecnologia"] = self.tecnologia.value
        return dicionario_base

    @classmethod
    def de_dicionario(cls, dicionario_do_ativo):
        return cls(
            dicionario_do_ativo["id"],
            dicionario_do_ativo["nome"],
            Setor(dicionario_do_ativo["setor"]),
            dicionario_do_ativo["responsavel"],
            StatusDoAtivo(dicionario_do_ativo["status"]),
            Cor(dicionario_do_ativo["cor"]),
            Tecnologia(dicionario_do_ativo["tecnologia"]),
        )


class DadoInvalidoError(Exception):
    pass


class StatusDoAtivo(Enum):
    ATIVO = 1
    INATIVO = 2
    EM_MANUTENCAO = 3


class NivelDaVulnerabilidade(Enum):
    BAIXO = 1
    MEDIO = 2
    ALTO = 3
    CRITICO = 4


class Setor(Enum):
    TI = 1
    FINANCEIRO = 2
    MARKETING = 3
    RH = 4
    JURIDICO = 5


class Cor(Enum):
    COLORIDA = 1
    PRETA_E_BRANCA = 2


class Tecnologia(Enum):
    TINTA = 1
    LASER = 2


class StatusDaVuln(Enum):
    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3
    ACEITA = 4


MAPA_DE_TIPOS = {
    "Notebook": Notebook,
    "Servidor": Servidor,
    "Roteador": Roteador,
    "Impressora": Impressora,
}

OPCOES_MENU = {"1": "Notebook", "2": "Servidor", "3": "Roteador", "4": "Impressora"}


def validar_nome_responsavel(nome):

    if not nome:
        raise DadoInvalidoError("Este campo não pode ser vazio.")
    if nome.isnumeric():
        raise DadoInvalidoError("Este campo não pode ser composto apenas por números.")


def pedir_info(mensagem):

    info = None
    while info is None:

        info = input(mensagem).strip()

        try:
            validar_nome_responsavel(info)
            return info
        except DadoInvalidoError as erro:
            print(erro)
            info = None


def pedir_status(mensagem):

    status = None

    while status is None:

        try:
            print("""
            Status:

            ATIVO - 1
            INATIVO - 2
            EM_MANUTENCAO - 3
            """)

            status_digitado = input(mensagem).strip()
            status = validar_status(status_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return status


def validar_status(status_digitado):

    if status_digitado == "1":
        return StatusDoAtivo.ATIVO

    elif status_digitado == "2":
        return StatusDoAtivo.INATIVO

    elif status_digitado == "3":
        return StatusDoAtivo.EM_MANUTENCAO

    else:
        raise DadoInvalidoError("Status inválido. Tente novamente.")


def pedir_status_vulnerabilidade(mensagem):

    status_tratamento = None

    while status_tratamento is None:

        try:
            print("""
            Status da vulnerabilidade:

            ABERTA - 1
            EM TRATAMENTO - 2
            CORRIGIDA - 3
            ACEITA - 4
            """)

            status_digitado = input(mensagem).strip()
            status_tratamento = validar_status_vulnerabilidade(status_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return status_tratamento


def validar_status_vulnerabilidade(status_digitado):

    if status_digitado == "1":
        return StatusDaVuln.ABERTA
    elif status_digitado == "2":
        return StatusDaVuln.EM_TRATAMENTO
    elif status_digitado == "3":
        return StatusDaVuln.CORRIGIDA
    elif status_digitado == "4":
        return StatusDaVuln.ACEITA
    else:
        raise DadoInvalidoError("Status inválido. Tente novamente.")


def pedir_setor(mensagem):

    setor = None

    while setor is None:

        try:
            print("""
            Setor:

            TI - 1
            FINANCEIRO - 2
            MARKETING - 3
            RH - 4
            JURIDICO - 5
            """)

            setor_digitado = input(mensagem).strip()
            setor = validar_setor(setor_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return setor


def validar_setor(setor_digitado):

    if setor_digitado == "1":
        return Setor.TI

    elif setor_digitado == "2":
        return Setor.FINANCEIRO

    elif setor_digitado == "3":
        return Setor.MARKETING

    elif setor_digitado == "4":
        return Setor.RH

    elif setor_digitado == "5":
        return Setor.JURIDICO

    else:
        raise DadoInvalidoError("Setor inválido. Tente novamente.")


def pedir_float(mensagem):
    while True:
        try:
            numero = input(mensagem).strip()

            if not numero:
                raise DadoInvalidoError("Este campo não pode ser vazio. Tente novamente.")

            if float(numero) <= 0:
                raise DadoInvalidoError(
                    "Este campo não pode ser nulo ou negativo. Tente novamente."
                )

            return float(numero)

        except ValueError:
            print("Digite um número válido")

        except DadoInvalidoError as erro:
            print(erro)


def pedir_int(mensagem):

    while True:
        try:
            numero_int = input(mensagem).strip()

            if not numero_int:
                raise DadoInvalidoError("Este campo não pode ser vazio. Tente novamente.")

            if int(numero_int) <= 0:
                raise DadoInvalidoError(
                    "Este campo não pode ser nulo ou negativo. Tente novamente."
                )

            return int(numero_int)

        except ValueError:
            print("Digite um número válido")

        except DadoInvalidoError as erro:
            print(erro)


def pedir_id_disponivel(ativos):

    while True:

        ID_do_ativo = pedir_int("Digite o ID do ativo: ")
        if encontrar_ativo_por_id(ID_do_ativo, ativos) is None:
            return ID_do_ativo

        print("Já existe um ativo cadastrado com este ID. Tente outro.")


def pedir_tipo(mensagem):

    tipo = None

    while tipo is None:

        try:
            print("Tipos de ativo:")
            for numero, nome in OPCOES_MENU.items():
                print(f"{numero} - {nome}")

            tipo_digitado = input(mensagem).strip()
            tipo = validar_tipo(tipo_digitado)

        except DadoInvalidoError as erro:
            print(erro)

    return tipo


def validar_tipo(tipo_digitado):

    if tipo_digitado == "1":
        return Notebook

    elif tipo_digitado == "2":
        return Servidor

    elif tipo_digitado == "3":
        return Roteador

    elif tipo_digitado == "4":
        return Impressora

    else:
        raise DadoInvalidoError("Tipo inválido. Tente novamente.")


def cadastro_notebook():

    so = pedir_info("Digite o sistema operacional do ativo: ")
    tela = pedir_float("Digite o tamanho da tela em polegadas: ")

    return so, tela


def cadastro_roteador():

    portas = pedir_int("Digite a quantidade de portas do roteador: ")
    velocidade = pedir_int("Digite a velocidade do roteador em MB: ")

    return portas, velocidade


def cadastro_servidor():

    ram = pedir_int("Digite a quantidade de RAM do Servidor em GB: ")
    armazenamento = pedir_float("Digite a quantidade de armazenamento do Servidor em T: ")

    return ram, armazenamento


def validar_cor(opcao):

    if opcao == "1":
        return Cor.COLORIDA
    elif opcao == "2":
        return Cor.PRETA_E_BRANCA

    else:
        raise DadoInvalidoError("Cor inválida. Tente novamente.")


def pedir_cor():

    cor = None
    while cor is None:

        try:
            print("""
            Qual é a cor do cartucho da impressora?

            1 - Colorido
            2 - Preto e branco
            """)
            opcao_cor = input("Escolha: ").strip()
            cor = validar_cor(opcao_cor)

        except DadoInvalidoError as erro:
            print(erro)

    return cor


def validar_tecnologia(opcao_tec):

    if opcao_tec == "1":
        return Tecnologia.TINTA
    elif opcao_tec == "2":
        return Tecnologia.LASER
    else:
        raise DadoInvalidoError("Tecnologia inválida. Tente novamente.")


def pedir_tecnologia():

    tecnologia = None
    while tecnologia is None:

        try:
            print("""
            Tecnologias de impressão:

            1 - Tinta
            2 - Laser
            """)
            opcao_tec = input("Qual é a tecnologia da impressão? ")
            tecnologia = validar_tecnologia(opcao_tec)

        except DadoInvalidoError as erro:
            print(erro)

    return tecnologia


def cadastro_impressora():
    cor = pedir_cor()
    tecnologia = pedir_tecnologia()
    return cor, tecnologia


def cadastrar_ativo(ativos):

    tipo = pedir_tipo("Digite o tipo do ativo: ")
    ID_do_ativo = pedir_id_disponivel(ativos)
    nome_ativo = pedir_info("Digite o nome do ativo: ")
    setor = pedir_setor("Digite o setor do ativo: ")
    responsavel = pedir_info("Digite o nome do responsável pelo ativo: ")
    status = pedir_status("Digite o status do ativo: ")

    if tipo is Notebook:
        so, tela = cadastro_notebook()
        ativo = Notebook(ID_do_ativo, nome_ativo, setor, responsavel, status, so, tela)

    elif tipo is Roteador:
        portas, velocidade = cadastro_roteador()
        ativo = Roteador(ID_do_ativo, nome_ativo, setor, responsavel, status, portas, velocidade)

    elif tipo is Servidor:
        ram, armazenamento = cadastro_servidor()
        ativo = Servidor(ID_do_ativo, nome_ativo, setor, responsavel, status, ram, armazenamento)

    elif tipo is Impressora:
        cor, tecnologia = cadastro_impressora()
        ativo = Impressora(ID_do_ativo, nome_ativo, setor, responsavel, status, cor, tecnologia)

    print("Ativo cadastrado com sucesso!")
    print(ativo.exibir_detalhes())
    return ativo


def encontrar_ativo_por_id(ID, ativos):
    return ativos.get(ID)


def encontrar_ativo_por_nome(nome, ativos):

    encontrados = []

    for ativo in ativos.values():
        if nome.lower() in ativo.nome.lower():
            encontrados.append(ativo)

    return encontrados


def encontrar_ativos_por_status(status, ativos):
    encontrados = []
    for ativo in ativos.values():
        if ativo.status == status:
            encontrados.append(ativo)
    return encontrados


def listar_ativos_por_tipo(classe, ativos):

    encontrados = []

    for ativo in ativos.values():
        if isinstance(ativo, classe):
            encontrados.append(ativo)

    return encontrados


def mostrar_vulnerabilidade(vulnerabilidade):

    print(f"""
    Vulnerabilidade: {vulnerabilidade.nome_vulnerabilidade}
    Tipo: {vulnerabilidade.tipo}
    Nível: {vulnerabilidade.nivel.name.lower()}
    Status: {vulnerabilidade.status_tratamento.name.lower()}
    """)


def editar_ativo(ativos):

    id_ativo = pedir_int("Digite o ID do ativo que deseja editar: ")

    ativo_encontrado = encontrar_ativo_por_id(id_ativo, ativos)

    if not ativo_encontrado:
        print("Nenhum ativo com este ID cadastrado.")
        return

    print(f"""Dados atuais do ativo:
    ID: {ativo_encontrado.id}
    Nome: {ativo_encontrado.nome}
    Responsável: {ativo_encontrado.responsavel}
    Tipo: {type(ativo_encontrado).__name__}
    Setor: {ativo_encontrado.setor.name}
    Status: {ativo_encontrado.status.name}
    """)

    while True:
        print("""
        MENU DE EDIÇÃO
        1 - Editar responsável
        2 - Editar status
        3 - Editar setor
        4 - Editar detalhes específicos
        5 - Editar tipo
        6 - Voltar""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            novo_responsavel = pedir_info("Digite o novo nome do responsável pelo ativo: ")
            ativo_encontrado.responsavel = novo_responsavel
            print(f"""
                Responsável atualizado com sucesso.
                Novo responsável: {novo_responsavel}.
                """)

        elif opcao == "2":
            novo_status = pedir_status("Digite o novo status do ativo: ")
            ativo_encontrado.status = novo_status
            print(f"""
                Status do ativo atualizado com sucesso.
                Status atual: {novo_status.name}.
                """)

        elif opcao == "3":
            novo_setor = pedir_setor("Digite o novo setor do ativo: ")
            ativo_encontrado.setor = novo_setor
            print(f"""
                Setor do ativo atualizado com sucesso.
                Setor atual: {novo_setor.name}.
                """)

        elif opcao == "4":

            if isinstance(ativo_encontrado, Notebook):
                ativo_encontrado.sistema_operacional = pedir_info("Novo SO: ")
                ativo_encontrado.tela = pedir_float("Nova tela: ")

            elif isinstance(ativo_encontrado, Roteador):
                ativo_encontrado.portas = pedir_int("Nova quantidade de portas: ")
                ativo_encontrado.velocidade = pedir_int("Nova velocidade em MB: ")

            elif isinstance(ativo_encontrado, Servidor):
                ativo_encontrado.ram = pedir_int("Digite a quantidade de RAM do Servidor em GB: ")
                ativo_encontrado.armazenamento = pedir_float(
                    "Digite a quantidade de armazenamento do Servidor em T: "
                )

            elif isinstance(ativo_encontrado, Impressora):
                ativo_encontrado.cor = pedir_cor()
                ativo_encontrado.tecnologia = pedir_tecnologia()

            print(f"""
            Detalhes específicos atualizados com sucesso!
            Ativo atualizado:
            {ativo_encontrado.exibir_detalhes()}
            """)

        elif opcao == "5":

            novo_tipo = pedir_tipo("Qual o novo tipo do ativo? ")

            if novo_tipo is Notebook:
                so, tela = cadastro_notebook()
                novo_ativo = Notebook(
                    id_ativo,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    so,
                    tela,
                )
            elif novo_tipo is Roteador:
                portas, velocidade = cadastro_roteador()
                novo_ativo = Roteador(
                    id_ativo,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    portas,
                    velocidade,
                )
            elif novo_tipo is Servidor:
                ram, armazenamento = cadastro_servidor()
                novo_ativo = Servidor(
                    id_ativo,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    ram,
                    armazenamento,
                )
            elif novo_tipo is Impressora:
                cor, tecnologia = cadastro_impressora()
                novo_ativo = Impressora(
                    id_ativo,
                    ativo_encontrado.nome,
                    ativo_encontrado.setor,
                    ativo_encontrado.responsavel,
                    ativo_encontrado.status,
                    cor,
                    tecnologia,
                )

            novo_ativo.vulnerabilidades = ativo_encontrado.vulnerabilidades
            ativos[id_ativo] = novo_ativo
            ativo_encontrado = novo_ativo
            print(f"""
                Tipo do ativo atualizado com sucesso!
                Tipo atual: {type(novo_ativo).__name__}.
                """)

        elif opcao == "6":
            print("Voltando...")
            break

        else:
            print("Opção inválida.")


def excluir_ativo(ativos):
    if ativos:
        id_a_excluir = pedir_int("Digite o ID do ativo que deseja excluir: ")
        ativo_encontrado = encontrar_ativo_por_id(id_a_excluir, ativos)

        if ativo_encontrado:

            if confirmar_exclusao(ativo_encontrado):
                del ativos[ativo_encontrado.id]
                salvar_dados(ativos)
                print("Ativo excluído com sucesso!")
            else:
                print("Exclusão cancelada.")

        else:
            print("Ativo não encontrado.")

    else:
        print("Nenhum ativo cadastrado.")


def confirmar_exclusao(ativo):

    print(f'Tem certeza que deseja excluir o ativo "{ativo.nome}" (ID {ativo.id})?')
    resposta = input('Digite "sim" para excluir ou tecle enter para voltar: ').strip().lower()

    if resposta == "sim":
        return True
    else:
        return False


def nivel_vulnerabilidade():

    nivel = None
    while nivel is None:
        print("""BAIXO - 1 \n MEDIO - 2 \n ALTO - 3""")

        nivel_digitado = input("Digite o nível da vulnerabilidade: ").strip()

        if nivel_digitado == "1":
            nivel = NivelDaVulnerabilidade.BAIXO
        elif nivel_digitado == "2":
            nivel = NivelDaVulnerabilidade.MEDIO
        elif nivel_digitado == "3":
            nivel = NivelDaVulnerabilidade.ALTO
        else:
            print("Nível inválido. Tente novamente.")
            continue

    return nivel


def salvar_catalogo(catalogo):

    catalogo_para_salvar = []

    for vulnerabilidade in catalogo.values():
        catalogo_para_salvar.append(vulnerabilidade.para_dicionario())

    try:
        with open(ARQUIVO_CATALOGO, "w", encoding="utf-8") as arquivo:
            json.dump(catalogo_para_salvar, arquivo, indent=4, ensure_ascii=False)
    except PermissionError:
        print("Erro de Persistência: Sem permissão para gravar no arquivo no computador.")
    except IOError:
        print("Erro de Persistência ao salvar os dados no arquivo.")


def carregar_catalogo():

    try:
        with open(ARQUIVO_CATALOGO, "r", encoding="utf-8") as arquivo:
            dados_brutos = json.load(arquivo)
            catalogo = {}

            for dicionario_vulnerabilidade in dados_brutos:
                vulnerabilidade = Vulnerabilidade.de_dicionario(dicionario_vulnerabilidade)
                catalogo[vulnerabilidade.id_vulnerabilidade] = vulnerabilidade

            return catalogo

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print("Aviso: ocorreu um erro no arquivo de dados. Criando um novo arquivo...")
        return {}


def salvar_dados(ativos):

    lista_para_salvar = []

    for ativo in ativos.values():
        lista_para_salvar.append(ativo.para_dicionario())

    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(lista_para_salvar, arquivo, indent=4, ensure_ascii=False)
    except PermissionError:
        print("Erro de Persistência: Sem permissão para gravar no arquivo no computador.")
    except IOError:
        print("Erro de Persistência ao salvar os dados no arquivo.")


def carregar_dados():

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados_brutos = json.load(arquivo)
            ativos_carregados = {}

            for ativo_dicionario in dados_brutos:
                tipo_string = ativo_dicionario["tipo"]
                classe = MAPA_DE_TIPOS[tipo_string]
                novo_ativo = classe.de_dicionario(ativo_dicionario)

                for vinculo in ativo_dicionario["vulnerabilidades"]:
                    id_vulnerabilidade = vinculo["id_vulnerabilidade"]
                    status_tratamento = StatusDaVuln(vinculo["status_tratamento"])
                    novo_ativo.vulnerabilidades[id_vulnerabilidade] = status_tratamento

                ativos_carregados[novo_ativo.id] = novo_ativo

            return ativos_carregados

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print("Aviso: ocorreu um erro no arquivo de dados. Criando um novo arquivo...")
        return {}
