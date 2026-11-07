-- NOTEBOOKS E SUAS TELAS
-- Selecione os ativos que são notebooks e mostre o nome, o responsável, a tela e o sistema operacional de cada um.
SELECT ativos.id, ativos.nome, ativos.responsavel, notebooks.tela, notebooks.sistema_operacional
FROM ativos
INNER JOIN notebooks ON notebooks.id_ativo = ativos.id;

-- VULNERABILIDADES E OS ATIVOS AFETADOS
-- Selecione cada vulnerabilidade com os ativos que ela afeta e o status do tratamento, ordenando pelo nome da vulnerabilidade.
SELECT vulnerabilidades.nome_vulnerabilidade, ativos.nome, vinculos.status_tratamento
FROM vulnerabilidades
INNER JOIN vinculos ON vinculos.id_vulnerabilidade = vulnerabilidades.id_vulnerabilidade
INNER JOIN ativos ON ativos.id = vinculos.id_ativo
ORDER BY vulnerabilidades.nome_vulnerabilidade;

-- VULNERABILIDADES SEM VÍNCULO
-- Selecione as vulnerabilidades do catálogo que não estão vinculadas a nenhum ativo.
SELECT vulnerabilidades.id_vulnerabilidade, vulnerabilidades.nome_vulnerabilidade, vulnerabilidades.cvss
FROM vulnerabilidades
LEFT JOIN vinculos ON vinculos.id_vulnerabilidade = vulnerabilidades.id_vulnerabilidade
WHERE vinculos.id_vulnerabilidade IS NULL;
