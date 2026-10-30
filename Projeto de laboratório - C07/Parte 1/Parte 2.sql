-- projeto c07 - banco de dados - parte 2
-- locadora de filmes

-- correção em relação à parte 1
-- o comentário recebido: "Cuidado com tipos de dados, como em
-- ano_lancamento e cpf e cep. Alguns desses atributos precisam de caracteres
-- especiais e portanto precisam ser do tipo string (VARCHAR ou CHAR)."
-- então esses viraram string:
-- cpf (Cliente e Funcionario): INT -> CHAR(15), por causa dos pontos e do traço
-- cep: INT -> CHAR(9), senão 03145-000 vira 3145000 e some o zero da frente
-- telefone: INT -> CHAR(15), mesma coisa, tem parêntese e traço
-- ano_lancamento: DATE -> CHAR(4), porque eu só preciso do ano
-- e os campos de dinheiro (salario, valor_multa e limite_desc_multa) passaram
-- pra DECIMAL, que não come os centavos.

-- ---------------------------------------------------------------------
-- ddl - criando o banco e as tabelas
-- ---------------------------------------------------------------------

DROP DATABASE IF EXISTS locadora_filmes;
CREATE DATABASE IF NOT EXISTS locadora_filmes;
USE locadora_filmes;

CREATE TABLE IF NOT EXISTS Cliente ( -- entidade forte, a chave é o próprio cpf
    cpf CHAR(15) NOT NULL, -- formato 000.000.000-00
    nome VARCHAR(45) NOT NULL,
    rua VARCHAR(45) NOT NULL,
    numero_casa INT NOT NULL,
    bairro VARCHAR(30) NOT NULL,
    cep CHAR(9) NOT NULL, -- formato 00000-000
    cidade VARCHAR(45) NOT NULL,
    PRIMARY KEY (cpf),
    CONSTRAINT uq_Cliente_numero_casa UNIQUE (numero_casa)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Telefone_Cliente ( -- 1:N, um cliente pode ter vários telefones
    telefone CHAR(15) NOT NULL, -- formato (00)00000-0000
    Cliente_cpf CHAR(15) NOT NULL,
    PRIMARY KEY (telefone, Cliente_cpf),
    CONSTRAINT fk_Telefone_Cliente_Cliente
        FOREIGN KEY (Cliente_cpf) REFERENCES Cliente (cpf) -- aponta pra um cliente que já existe
        ON DELETE CASCADE -- se o cliente sumir, o telefone vai junto
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Funcionario ( -- superclasse da herança
    idFuncionario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL,
    data_nascimento DATE NOT NULL,
    cpf CHAR(15) NOT NULL,
    salario DECIMAL(10,2) NOT NULL, -- 10 dígitos no total, 2 deles depois da vírgula
    PRIMARY KEY (idFuncionario),
    CONSTRAINT uq_Funcionario_cpf UNIQUE (cpf) -- não dá pra ter dois funcionários com o mesmo cpf
) ENGINE = InnoDB;

-- herança: cada subclasse virou uma tabela. a chave primária dela também é
-- chave estrangeira pra Funcionario, então ninguém entra como atendente ou
-- gerente sem existir antes como funcionário.
CREATE TABLE IF NOT EXISTS Funcionario_Atendente (
    Funcionario_idFuncionario INT NOT NULL,
    turno VARCHAR(10) NOT NULL,
    PRIMARY KEY (Funcionario_idFuncionario),
    CONSTRAINT fk_Funcionario_Atendente_Funcionario
        FOREIGN KEY (Funcionario_idFuncionario) REFERENCES Funcionario (idFuncionario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Funcionario_Gerente (
    Funcionario_idFuncionario INT NOT NULL,
    limite_desc_multa DECIMAL(10,2) NOT NULL DEFAULT 0.00, -- quanto de desconto na multa esse gerente pode dar. se o insert não disser nada, entra zero
    PRIMARY KEY (Funcionario_idFuncionario),
    CONSTRAINT fk_Funcionario_Gerente_Funcionario
        FOREIGN KEY (Funcionario_idFuncionario) REFERENCES Funcionario (idFuncionario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Categoria ( -- a classificação indicativa do filme
    idCategoria INT NOT NULL AUTO_INCREMENT,
    faixa_etaria VARCHAR(20) NOT NULL,
    PRIMARY KEY (idCategoria)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Ator (
    idAtor INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45) NOT NULL,
    PRIMARY KEY (idAtor)
) ENGINE = InnoDB;

-- autorrelacionamento: Filme_idFilme_sequencia aponta pro filme anterior da
-- sequência. aceita null porque a maioria dos filmes não é continuação de nada.
CREATE TABLE IF NOT EXISTS Filme (
    idFilme INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(45) NOT NULL,
    duracao_min INT NOT NULL,
    ano_lancamento CHAR(4) NOT NULL, -- só o ano, por isso string
    Categoria_idCategoria INT NOT NULL,
    Filme_idFilme_sequencia INT NULL,
    PRIMARY KEY (idFilme),
    CONSTRAINT fk_Filme_Categoria
        FOREIGN KEY (Categoria_idCategoria) REFERENCES Categoria (idCategoria)
        ON DELETE RESTRICT -- trava o delete de categoria que ainda tem filme, é o contrário do cascade
        ON UPDATE CASCADE,
    CONSTRAINT fk_Filme_Filme
        FOREIGN KEY (Filme_idFilme_sequencia) REFERENCES Filme (idFilme)
        ON DELETE SET NULL -- se o primeiro sumir a continuação fica sem o link, mas não some
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Atuacao ( -- tabela do meio do N:M entre Ator e Filme
    Ator_idAtor INT NOT NULL,
    Filme_idFilme INT NOT NULL,
    papel VARCHAR(20) NOT NULL,
    PRIMARY KEY (Ator_idAtor, Filme_idFilme),
    CONSTRAINT fk_Atuacao_Ator
        FOREIGN KEY (Ator_idAtor) REFERENCES Ator (idAtor)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_Atuacao_Filme
        FOREIGN KEY (Filme_idFilme) REFERENCES Filme (idFilme)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Locacao ( -- 1:N com Cliente e 1:N com Funcionario
    idLocacao INT NOT NULL AUTO_INCREMENT,
    data_locacao DATE NOT NULL,
    data_prev_devolucao DATE NOT NULL,
    Cliente_cpf CHAR(15) NOT NULL,
    Funcionario_idFuncionario INT NOT NULL,
    PRIMARY KEY (idLocacao),
    CONSTRAINT fk_Locacao_Cliente
        FOREIGN KEY (Cliente_cpf) REFERENCES Cliente (cpf)
        ON DELETE RESTRICT -- não deixa apagar cliente que tem locação no histórico
        ON UPDATE CASCADE,
    CONSTRAINT fk_Locacao_Funcionario
        FOREIGN KEY (Funcionario_idFuncionario) REFERENCES Funcionario (idFuncionario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Posse ( -- tabela do meio do N:M entre Locacao e Filme
    Locacao_idLocacao INT NOT NULL,
    Filme_idFilme INT NOT NULL,
    PRIMARY KEY (Locacao_idLocacao, Filme_idFilme),
    CONSTRAINT fk_Posse_Locacao
        FOREIGN KEY (Locacao_idLocacao) REFERENCES Locacao (idLocacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_Posse_Filme
        FOREIGN KEY (Filme_idFilme) REFERENCES Filme (idFilme)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Devolucao ( -- 1:1 com Locacao
    Locacao_idLocacao INT NOT NULL, -- é chave primária e estrangeira ao mesmo tempo, por isso cada locação só tem uma devolução
    data_devolucao DATE NOT NULL,
    valor_multa DECIMAL(10,2) NOT NULL DEFAULT 0.00, -- devolveu no prazo, fica 0.00
    PRIMARY KEY (Locacao_idLocacao),
    CONSTRAINT fk_Devolucao_Locacao
        FOREIGN KEY (Locacao_idLocacao) REFERENCES Locacao (idLocacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Log_Locacao ( -- extra: histórico das locações. quem escreve aqui é o trigger
    idLog INT NOT NULL AUTO_INCREMENT,
    Locacao_idLocacao INT NOT NULL,
    Cliente_cpf CHAR(15) NOT NULL,
    registrado_em DATETIME NOT NULL,
    operacao VARCHAR(20) NOT NULL,
    PRIMARY KEY (idLog)
) ENGINE = InnoDB;

SHOW TABLES; -- só pra ver se criou tudo

-- ---------------------------------------------------------------------
-- dml - colocando os dados
-- 5 registros em cada tabela, no mínimo. a ordem segue as chaves
-- estrangeiras: primeiro quem não depende de ninguém, depois o resto.
-- ---------------------------------------------------------------------

INSERT INTO Cliente (cpf, nome, rua, numero_casa, bairro, cep, cidade) VALUES
('123.456.789-01', 'Ana Beatriz Moraes', 'Rua das Acacias', 120, 'Centro', '37540-000', 'Santa Rita do Sapucai'),
('234.567.890-12', 'Bruno Carvalho', 'Av. Sao Paulo', 85, 'Jardim Alvorada', '37540-010', 'Santa Rita do Sapucai'),
('345.678.901-23', 'Carla Nogueira', 'Rua Minas Gerais', 402, 'Bela Vista', '37540-020', 'Santa Rita do Sapucai'),
('456.789.012-34', 'Diego Ferraz', 'Rua Sete de Setembro', 33, 'Centro', '37540-000', 'Santa Rita do Sapucai'),
('567.890.123-45', 'Elisa Prado', 'Rua dos Ipes', 210, 'Vila Rica', '37540-030', 'Pouso Alegre');

INSERT INTO Telefone_Cliente (telefone, Cliente_cpf) VALUES -- a Elisa tem dois números, é o 1:N na prática
('(35)99812-4455', '123.456.789-01'),
('(35)99733-1020', '234.567.890-12'),
('(35)99654-7788', '345.678.901-23'),
('(35)99501-3366', '456.789.012-34'),
('(35)99477-9012', '567.890.123-45'),
('(35)3471-2200', '567.890.123-45');

INSERT INTO Funcionario (nome, data_nascimento, cpf, salario) VALUES -- os 5 primeiros viram atendentes, os 5 últimos gerentes
('Laís', '2005-03-14', '111.222.333-01', 2100.00),
('Pedro', '2004-11-02', '111.222.333-02', 2050.00),
('Helena Souza', '2003-07-23', '111.222.333-03', 1980.00),
('Igor Martins', '2000-01-30', '111.222.333-04', 2150.00),
('Juliana Reis', '2002-05-19', '111.222.333-05', 2000.00),
('Karen Duarte', '1988-09-08', '111.222.333-06', 4800.00),
('Lucas Andrade', '1985-02-17', '111.222.333-07', 5200.00),
('Marina Vieira', '1990-12-05', '111.222.333-08', 4950.00),
('Nelson Barbosa', '1983-06-27', '111.222.333-09', 5600.00),
('Otavio Pinheiro', '1992-04-11', '111.222.333-10', 4700.00);

INSERT INTO Funcionario_Atendente (Funcionario_idFuncionario, turno) VALUES -- cada funcionário aparece em uma subclasse só
(1, 'Manha'),
(2, 'Tarde'),
(3, 'Noite'),
(4, 'Manha'),
(5, 'Noite');

INSERT INTO Funcionario_Gerente (Funcionario_idFuncionario, limite_desc_multa) VALUES
(6, 50.00),
(7, 80.00),
(8, 60.00),
(9, 120.00),
(10, 45.00);

INSERT INTO Categoria (faixa_etaria) VALUES
('Livre'),
('10 anos'),
('12 anos'),
('14 anos'),
('16 anos'),
('18 anos');

INSERT INTO Filme (titulo, duracao_min, ano_lancamento, Categoria_idCategoria) VALUES -- o autorrelacionamento eu preencho logo abaixo, com update
('O Senhor dos Aneis', 178, '2001', 3),
('O Senhor dos Aneis II', 179, '2002', 3),
('O Senhor dos Aneis III', 201, '2003', 3),
('Procurando Nemo', 100, '2003', 1),
('Matrix', 136, '1999', 5),
('Cidade de Deus', 130, '2002', 6),
('A Origem', 148, '2010', 4),
('Toy Story', 81, '1995', 1);

INSERT INTO Ator (nome) VALUES
('Elijah Wood'),
('Ian McKellen'),
('Keanu Reeves'),
('Leonardo DiCaprio'),
('Alexandre Rodrigues'),
('Tom Hanks');

INSERT INTO Atuacao (Ator_idAtor, Filme_idFilme, papel) VALUES -- N:M entre Ator e Filme
(1, 1, 'Frodo'),
(1, 2, 'Frodo'),
(1, 3, 'Frodo'),
(2, 1, 'Gandalf'),
(2, 3, 'Gandalf'),
(3, 5, 'Neo'),
(4, 7, 'Cobb'),
(5, 6, 'Buscape'),
(6, 8, 'Woody');

INSERT INTO Locacao (data_locacao, data_prev_devolucao, Cliente_cpf, Funcionario_idFuncionario) VALUES
('2026-09-01', '2026-09-04', '123.456.789-01', 1),
('2026-09-03', '2026-09-06', '234.567.890-12', 2),
('2026-09-05', '2026-09-08', '345.678.901-23', 3),
('2026-09-10', '2026-09-13', '123.456.789-01', 4),
('2026-09-12', '2026-09-15', '456.789.012-34', 5),
('2026-09-20', '2026-09-23', '567.890.123-45', 1);

INSERT INTO Posse (Locacao_idLocacao, Filme_idFilme) VALUES -- N:M entre Locacao e Filme
(1, 1),
(1, 5),
(2, 4),
(3, 6),
(3, 7),
(4, 2),
(5, 8),
(6, 3),
(6, 5);

INSERT INTO Devolucao (Locacao_idLocacao, data_devolucao, valor_multa) VALUES -- as locações 5 e 6 ainda estão em aberto, por isso não entram aqui
(1, '2026-09-04', 0.00),
(2, '2026-09-08', 5.00),
(3, '2026-09-08', 0.00),
(4, '2026-09-16', 7.50);

-- ---------------------------------------------------------------------
-- dml - mexendo nos dados (update e delete)
-- cada comando tem o motivo logo acima dele
-- ---------------------------------------------------------------------

-- update pra preencher o autorrelacionamento de Filme. os ids só existem
-- depois que o auto_increment roda, então ligamos cada filme na continuação
-- dele agora, e não no insert.
UPDATE Filme SET Filme_idFilme_sequencia = 1 WHERE idFilme = 2;
UPDATE Filme SET Filme_idFilme_sequencia = 2 WHERE idFilme = 3;

-- update pra dar 8% de aumento só pros atendentes. com um comando só o banco
-- mexe nos cinco de uma vez
UPDATE Funcionario
SET salario = salario * 1.08
WHERE idFuncionario IN (SELECT Funcionario_idFuncionario FROM Funcionario_Atendente);

-- update pra arrumar um cadastro. o cliente mudou de endereço, então
-- atualizamos o registro dele em vez de cadastrar outro.
UPDATE Cliente
SET rua = 'Rua Coronel Joaquim Neto', numero_casa = 77, bairro = 'Centro'
WHERE cpf = '456.789.012-34';

-- update pra esticar o prazo de uma locação em dois dias.
UPDATE Locacao
SET data_prev_devolucao = DATE_ADD(data_prev_devolucao, INTERVAL 2 DAY)
WHERE idLocacao = 6;

-- delete de um telefone que o cliente não usa mais.
DELETE FROM Telefone_Cliente
WHERE telefone = '(35)3471-2200' AND Cliente_cpf = '567.890.123-45';

-- delete pra mostrar o on delete cascade acontecendo. apagando o Tom Hanks, a
-- participação dele em Atuacao some junto e não fica registro solto.
DELETE FROM Ator WHERE idAtor = 6;

SELECT * FROM Atuacao WHERE Ator_idAtor = 6; -- confere o cascade: tem que vir vazio

-- ---------------------------------------------------------------------
-- dcl - role e usuários
-- a role guarda as permissões do cargo. os dois usuários recebem a role em
-- vez de receber permissão uma por uma.
-- ---------------------------------------------------------------------

DROP ROLE IF EXISTS 'atendente_locadora';
CREATE ROLE 'atendente_locadora';

-- o atendente consulta, cadastra e corrige, mas não apaga registro nem mexe
-- na estrutura do banco.
GRANT SELECT, INSERT, UPDATE ON locadora_filmes.* TO 'atendente_locadora';
GRANT EXECUTE ON locadora_filmes.* TO 'atendente_locadora'; -- pra conseguir chamar as procedures e functions
GRANT DELETE ON locadora_filmes.Telefone_Cliente TO 'atendente_locadora'; -- essa é em nível de tabela, só na Telefone_Cliente

DROP USER IF EXISTS 'lais_atendente'@'localhost';
DROP USER IF EXISTS 'pedro_atendente'@'localhost';

CREATE USER 'lais_atendente'@'localhost' IDENTIFIED BY 'Senha@123';
CREATE USER 'pedro_atendente'@'localhost' IDENTIFIED BY 'Senha@456';

GRANT 'atendente_locadora' TO 'lais_atendente'@'localhost'; -- ligando os usuários na role
GRANT 'atendente_locadora' TO 'pedro_atendente'@'localhost';

-- role padrão. sem isso o usuário entra sem permissão nenhuma ativa
SET DEFAULT ROLE 'atendente_locadora' TO 'lais_atendente'@'localhost';
SET DEFAULT ROLE 'atendente_locadora' TO 'pedro_atendente'@'localhost';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'atendente_locadora'; -- vendo o que a role pode fazer

-- revoke tirando o delete que tinhamos dado. ele precisa ser no mesmo nível
-- do grant, e como demos na tabela Telefone_Cliente, é de lá que tiramos.
REVOKE DELETE ON locadora_filmes.Telefone_Cliente FROM 'atendente_locadora';

SHOW GRANTS FOR 'atendente_locadora'; -- agora sem o delete

-- ---------------------------------------------------------------------
-- dql - buscas com join
-- ---------------------------------------------------------------------

-- join no 1:1, Locacao x Devolucao. usamos left join na Devolucao pra aparecer
-- também o que ainda não foi devolvido, com null nas colunas da devolução.
SELECT
    locacao.idLocacao AS 'Locacao',
    cliente.nome AS 'Cliente',
    locacao.data_prev_devolucao AS 'Prazo',
    devolucao.data_devolucao AS 'Devolvido em',
    devolucao.valor_multa AS 'Multa'
FROM Locacao locacao
INNER JOIN Cliente cliente
    ON locacao.Cliente_cpf = cliente.cpf
LEFT JOIN Devolucao devolucao
    ON locacao.idLocacao = devolucao.Locacao_idLocacao
ORDER BY locacao.idLocacao;

-- join no 1:N, Cliente x Telefone_Cliente.
SELECT
    cliente.nome AS 'Cliente',
    cliente.cidade AS 'Cidade',
    telefone.telefone AS 'Telefone'
FROM Cliente cliente
INNER JOIN Telefone_Cliente telefone
    ON cliente.cpf = telefone.Cliente_cpf
ORDER BY cliente.nome;

-- outro 1:N, agora com group by: quantos filmes tem cada faixa etária.
SELECT
    categoria.faixa_etaria AS 'Faixa Etaria',
    COUNT(filme.idFilme) AS 'Qtd de Filmes'
FROM Categoria categoria
LEFT JOIN Filme filme
    ON categoria.idCategoria = filme.Categoria_idCategoria
GROUP BY categoria.idCategoria, categoria.faixa_etaria
ORDER BY COUNT(filme.idFilme) DESC;

-- join no N:M, Filme x Ator. são dois joins porque a ligação passa pela Atuacao.
SELECT
    filme.titulo AS 'Filme',
    filme.ano_lancamento AS 'Ano',
    ator.nome AS 'Ator',
    atuacao.papel AS 'Papel'
FROM Filme filme
INNER JOIN Atuacao atuacao
    ON filme.idFilme = atuacao.Filme_idFilme
INNER JOIN Ator ator
    ON atuacao.Ator_idAtor = ator.idAtor
ORDER BY filme.titulo, ator.nome;

-- essa aqui junta o 1:N, o N:M e a herança, que é um 1:1. mostra quem alugou
-- qual filme, com qual atendente e em que turno.
SELECT
    locacao.idLocacao AS 'Locacao',
    cliente.nome AS 'Cliente',
    filme.titulo AS 'Filme',
    funcionario.nome AS 'Atendente',
    atendente.turno AS 'Turno'
FROM Locacao locacao
INNER JOIN Cliente cliente
    ON locacao.Cliente_cpf = cliente.cpf
INNER JOIN Posse posse
    ON locacao.idLocacao = posse.Locacao_idLocacao
INNER JOIN Filme filme
    ON posse.Filme_idFilme = filme.idFilme
INNER JOIN Funcionario funcionario
    ON locacao.Funcionario_idFuncionario = funcionario.idFuncionario
INNER JOIN Funcionario_Atendente atendente
    ON funcionario.idFuncionario = atendente.Funcionario_idFuncionario
ORDER BY locacao.idLocacao, filme.titulo;

-- as duas subclasses da herança juntas: quem é atendente tem turno e o limite
-- de desconto fica null, quem é gerente é o contrário.
SELECT
    funcionario.nome AS 'Funcionario',
    atendente.turno AS 'Turno',
    gerente.limite_desc_multa AS 'Limite de desconto na multa'
FROM Funcionario funcionario
LEFT JOIN Funcionario_Atendente atendente
    ON funcionario.idFuncionario = atendente.Funcionario_idFuncionario
LEFT JOIN Funcionario_Gerente gerente
    ON funcionario.idFuncionario = gerente.Funcionario_idFuncionario
ORDER BY funcionario.nome;

-- autorrelacionamento: o filme e a continuação dele. a Filme entra duas vezes
-- na consulta, com apelidos diferentes.
SELECT
    filme_atual.titulo AS 'Filme',
    filme_anterior.titulo AS 'Continuacao de'
FROM Filme filme_atual
LEFT JOIN Filme filme_anterior
    ON filme_atual.Filme_idFilme_sequencia = filme_anterior.idFilme
ORDER BY filme_atual.idFilme;

-- subquery: clientes que alugaram mais de uma vez. a consulta de dentro
-- devolve a lista de cpfs e o in filtra por ela.
SELECT nome AS 'Cliente'
FROM Cliente
WHERE cpf IN (
    SELECT Cliente_cpf
    FROM Locacao
    GROUP BY Cliente_cpf
    HAVING COUNT(*) > 1
);

-- ---------------------------------------------------------------------
-- objetos programáveis
-- os quatro trabalham juntos em cima da mesma regra, a multa por atraso
-- ---------------------------------------------------------------------

-- function fn_calcular_multa, que cobra R$ 2,50 por dia de atraso.
-- usamos function porque ela só calcula e devolve um valor, e assim dá pra
-- chamar ela dentro de um select. a regra fica guardada num lugar só, então
-- se mudar o valor da diária mexemos em um ponto e pronto
DELIMITER $$

DROP FUNCTION IF EXISTS fn_calcular_multa$$

CREATE FUNCTION fn_calcular_multa(
    p_data_prevista DATE,
    p_data_devolucao DATE
)
RETURNS DECIMAL(10,2)
DETERMINISTIC -- mesma entrada, mesma saída
BEGIN
    DECLARE v_dias_atraso INT;
    DECLARE v_valor_da_diaria DECIMAL(10,2) DEFAULT 2.50;

    SET v_dias_atraso = DATEDIFF(p_data_devolucao, p_data_prevista);

    IF v_dias_atraso <= 0 THEN
        RETURN 0.00; -- devolveu no prazo ou antes
    ELSE
        RETURN v_dias_atraso * v_valor_da_diaria;
    END IF;
END$$

DELIMITER ;

SELECT -- testando a function
    fn_calcular_multa('2026-09-04', '2026-09-04') AS 'No prazo',
    fn_calcular_multa('2026-09-04', '2026-09-07') AS 'Atraso de 3 dias';

-- trigger trg_devolucao_calcula_multa, before insert na Devolucao.
-- fizemos pra multa não depender de alguém lembrar de calcular, assim todo insert
-- já entra com o valor certo. é before porque precisamos mexer no
-- NEW.valor_multa antes de gravar.
DELIMITER $$

DROP TRIGGER IF EXISTS trg_devolucao_calcula_multa$$

CREATE TRIGGER trg_devolucao_calcula_multa
BEFORE INSERT ON Devolucao
FOR EACH ROW
BEGIN
    DECLARE v_data_prevista DATE;

    SELECT data_prev_devolucao INTO v_data_prevista
    FROM Locacao
    WHERE idLocacao = NEW.Locacao_idLocacao;

    SET NEW.valor_multa = fn_calcular_multa(v_data_prevista, NEW.data_devolucao);
END$$

DELIMITER ;

-- trigger trg_locacao_auditoria, after insert na Locacao, é extra.
-- fizemos pra auditoria: toda locação nova fica registrada na Log_Locacao com
-- data e hora. é after porque o id da locação só existe depois que a linha
-- foi gravada.
DELIMITER $$

DROP TRIGGER IF EXISTS trg_locacao_auditoria$$

CREATE TRIGGER trg_locacao_auditoria
AFTER INSERT ON Locacao
FOR EACH ROW
BEGIN
    INSERT INTO Log_Locacao (Locacao_idLocacao, Cliente_cpf, registrado_em, operacao)
    VALUES (NEW.idLocacao, NEW.Cliente_cpf, NOW(), 'INSERT');
END$$

DELIMITER ;

INSERT INTO Locacao (data_locacao, data_prev_devolucao, Cliente_cpf, Funcionario_idFuncionario) VALUES -- testando o trigger: inserimos cinco locações e o log se preenche sozinho
('2026-10-01', '2026-10-04', '345.678.901-23', 2),
('2026-10-02', '2026-10-05', '123.456.789-01', 3),
('2026-10-03', '2026-10-06', '234.567.890-12', 1),
('2026-10-05', '2026-10-08', '456.789.012-34', 4),
('2026-10-06', '2026-10-09', '567.890.123-45', 5);

INSERT INTO Posse (Locacao_idLocacao, Filme_idFilme) VALUES -- os filmes que saíram nessas locações
(7, 4),
(8, 1),
(9, 5),
(10, 7),
(11, 2);

SELECT * FROM Log_Locacao; -- trigger

-- procedure sp_registrar_devolucao.
-- fizemos porque registrar uma devolução tem mais de um passo: ver se a locação
-- existe, se já não foi devolvida e se a data faz sentido, pra só então
-- inserir. é procedure e não function porque ela executa um insert, e
-- function não insere.
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_registrar_devolucao$$

CREATE PROCEDURE sp_registrar_devolucao(
    IN p_id_locacao INT,
    IN p_data_devolucao DATE
)
BEGIN
    DECLARE v_data_da_locacao DATE;
    DECLARE v_devolucoes_existentes INT DEFAULT 0;

    SELECT data_locacao INTO v_data_da_locacao -- essa locação existe?
    FROM Locacao
    WHERE idLocacao = p_id_locacao;

    IF v_data_da_locacao IS NULL THEN
        SELECT 'ERRO: essa locacao nao existe.' AS Resultado;

    ELSE
        SELECT COUNT(*) INTO v_devolucoes_existentes -- já tem devolução? o 1:1 só deixa uma
        FROM Devolucao
        WHERE Locacao_idLocacao = p_id_locacao;

        IF v_devolucoes_existentes > 0 THEN
            SELECT 'ERRO: essa locacao ja foi devolvida.' AS Resultado;

        ELSEIF p_data_devolucao < v_data_da_locacao THEN
            SELECT 'ERRO: a data de devolucao e anterior a da locacao.' AS Resultado;

        ELSE
            INSERT INTO Devolucao (Locacao_idLocacao, data_devolucao, valor_multa)
            VALUES (p_id_locacao, p_data_devolucao, 0.00); -- o 0.00 é só valor de partida, o trigger troca pelo certo

            SELECT 'Devolucao registrada com sucesso.' AS Resultado;
        END IF;
    END IF;
END$$

DELIMITER ;

-- testando a procedure e o trigger da multa
CALL sp_registrar_devolucao(5, '2026-09-18'); -- 3 dias de atraso dá 7,50
CALL sp_registrar_devolucao(5, '2026-09-19'); -- recusa: já foi devolvida
CALL sp_registrar_devolucao(99, '2026-09-19'); -- recusa: nem existe

SELECT * FROM Devolucao;

-- view vw_locacoes_detalhadas.
-- fizemos porque aquela consulta que junta tudo tem vários joins e teriamos que
-- reescrever ela toda hora. e de brinde ela protege as tabelas, porque quem
-- usa a view não enxerga coluna tipo o salário do funcionário.
CREATE OR REPLACE VIEW vw_locacoes_detalhadas AS (
    SELECT
        locacao.idLocacao AS 'id_locacao',
        cliente.nome AS 'cliente',
        filme.titulo AS 'filme',
        funcionario.nome AS 'atendente',
        locacao.data_locacao AS 'data_locacao',
        locacao.data_prev_devolucao AS 'prazo',
        devolucao.data_devolucao AS 'data_devolucao',
        devolucao.valor_multa AS 'multa'
    FROM Locacao locacao
    INNER JOIN Cliente cliente
        ON locacao.Cliente_cpf = cliente.cpf
    INNER JOIN Posse posse
        ON locacao.idLocacao = posse.Locacao_idLocacao
    INNER JOIN Filme filme
        ON posse.Filme_idFilme = filme.idFilme
    INNER JOIN Funcionario funcionario
        ON locacao.Funcionario_idFuncionario = funcionario.idFuncionario
    LEFT JOIN Devolucao devolucao
        ON locacao.idLocacao = devolucao.Locacao_idLocacao
);

SELECT * FROM vw_locacoes_detalhadas; -- a view se consulta igual tabela
SELECT * FROM vw_locacoes_detalhadas WHERE multa > 0;

-- ---------------------------------------------------------------------
-- implementações extras
-- ---------------------------------------------------------------------

-- tcl: esticamos o prazo de duas locações dentro de uma transação. o savepoint
-- marca um ponto no meio, o rollback to desfaz só o que veio depois dele e o
-- commit confirma o resto
START TRANSACTION;

UPDATE Locacao
SET data_prev_devolucao = DATE_ADD(data_prev_devolucao, INTERVAL 1 DAY)
WHERE idLocacao = 6;

SAVEPOINT prorrogou_a_primeira;

UPDATE Locacao
SET data_prev_devolucao = DATE_ADD(data_prev_devolucao, INTERVAL 1 DAY)
WHERE idLocacao = 7;

ROLLBACK TO prorrogou_a_primeira; -- desfaz só a segunda

COMMIT;

SELECT idLocacao, data_prev_devolucao FROM Locacao WHERE idLocacao IN (6, 7); -- a 6 ganhou um dia, a 7 ficou igual

-- índice na data de devolução prevista, que é por onde a locadora procura as
-- pendências. deixa a busca mais rápida.
CREATE INDEX idx_locacao_prazo ON Locacao (data_prev_devolucao);

SHOW INDEX FROM Locacao;

SELECT idLocacao, Cliente_cpf, data_prev_devolucao
FROM Locacao
WHERE data_prev_devolucao < '2026-10-01'
ORDER BY data_prev_devolucao;

-- alter table pra adicionar uma coluna nova sem perder os dados que já
-- estavam lá. o enum só deixa entrar 'Sim' ou 'Nao'.
ALTER TABLE Filme
ADD COLUMN disponivel ENUM('Sim', 'Nao') NOT NULL DEFAULT 'Sim';

UPDATE Filme SET disponivel = 'Nao' WHERE idFilme = 6;

SELECT titulo, ano_lancamento, disponivel FROM Filme;

-- conferindo quantos registros cada tabela ficou no final
SELECT COUNT(*) AS Cliente FROM Cliente;
SELECT COUNT(*) AS Telefone_Cliente FROM Telefone_Cliente;
SELECT COUNT(*) AS Funcionario FROM Funcionario;
SELECT COUNT(*) AS Funcionario_Atendente FROM Funcionario_Atendente;
SELECT COUNT(*) AS Funcionario_Gerente FROM Funcionario_Gerente;
SELECT COUNT(*) AS Categoria FROM Categoria;
SELECT COUNT(*) AS Ator FROM Ator;
SELECT COUNT(*) AS Filme FROM Filme;
SELECT COUNT(*) AS Atuacao FROM Atuacao;
SELECT COUNT(*) AS Locacao FROM Locacao;
SELECT COUNT(*) AS Posse FROM Posse;
SELECT COUNT(*) AS Devolucao FROM Devolucao;
SELECT COUNT(*) AS Log_Locacao FROM Log_Locacao;

SHOW TRIGGERS; -- os objetos programáveis que ficaram criados