PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS ativos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('Notebook', 'Impressora', 'Roteador', 'Servidor')),
    setor INTEGER NOT NULL CHECK (setor IN (1, 2, 3, 4, 5)),
    responsavel TEXT NOT NULL,
    status INTEGER NOT NULL CHECK (status IN (1, 2, 3)),
    fator_exposicao REAL NOT NULL CHECK (fator_exposicao > 0)
);

CREATE TABLE IF NOT EXISTS notebooks (
    id_ativo INTEGER PRIMARY KEY,
    tela REAL NOT NULL,
    sistema_operacional TEXT NOT NULL,
    FOREIGN KEY (id_ativo) REFERENCES ativos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS impressoras (
    id_ativo INTEGER PRIMARY KEY,
    tecnologia INTEGER NOT NULL CHECK (tecnologia IN (1, 2)),
    cor INTEGER NOT NULL CHECK (cor IN (1, 2)),
    FOREIGN KEY (id_ativo) REFERENCES ativos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS roteadores (
    id_ativo INTEGER PRIMARY KEY,
    portas INTEGER NOT NULL CHECK (portas > 0),
    velocidade INTEGER NOT NULL CHECK (velocidade > 0),
    FOREIGN KEY (id_ativo) REFERENCES ativos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS servidores (
    id_ativo INTEGER PRIMARY KEY,
    ram INTEGER NOT NULL CHECK (ram > 0),
    armazenamento REAL NOT NULL CHECK (armazenamento > 0),
    FOREIGN KEY (id_ativo) REFERENCES ativos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vulnerabilidades (
    id_vulnerabilidade INTEGER PRIMARY KEY,
    nome_vulnerabilidade TEXT NOT NULL,
    cvss REAL NOT NULL CHECK (cvss >= 0 AND cvss <= 10)
);

CREATE TABLE IF NOT EXISTS vinculos (
    id_ativo INTEGER NOT NULL,
    id_vulnerabilidade INTEGER NOT NULL,
    status_tratamento  INTEGER NOT NULL CHECK (status_tratamento IN (1, 2, 3, 4)),
    PRIMARY KEY (id_ativo, id_vulnerabilidade),
    FOREIGN KEY (id_ativo) REFERENCES ativos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_vulnerabilidade) REFERENCES vulnerabilidades(id_vulnerabilidade) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dependencias (
    id_ativo_que_depende INTEGER NOT NULL,
    id_ativo_do_qual_depende INTEGER NOT NULL,
    fracao REAL NOT NULL CHECK (fracao > 0 AND fracao < 1),
    PRIMARY KEY (id_ativo_que_depende, id_ativo_do_qual_depende),
    CHECK (id_ativo_que_depende != id_ativo_do_qual_depende),
    FOREIGN KEY (id_ativo_que_depende) REFERENCES ativos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_ativo_do_qual_depende) REFERENCES ativos(id) ON DELETE CASCADE
);