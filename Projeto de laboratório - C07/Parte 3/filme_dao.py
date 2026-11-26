from dataclasses import dataclass #gera automaticamente __init__, __repr__ e __eq__ para Filme
from typing import Optional
from mysql.connector import Error, errorcode
from conexao import get_conexao

@dataclass()
class Filme:
    idFilme: Optional[int] #aqui usa o auto_increment
    titulo: str
    duracao_min: int
    ano_lancamento: str
    Categoria_idCategoria: int
    Filme_idFilme_sequencia: Optional[int]
    disponivel: str = "Sim"

class FilmeDAO:
    def criar(self, filme: Filme) -> int: #a chave é gerado pelo bd, por isso filme: Filme
        sql = ("INSERT INTO Filme (titulo, duracao_min, ano_lancamento, "
               "Categoria_idCategoria, Filme_idFilme_sequencia, disponivel) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (filme.titulo, filme.duracao_min,
                                 filme.ano_lancamento, filme.Categoria_idCategoria,
                                 filme.Filme_idFilme_sequencia, filme.disponivel))
            conn.commit()
            return int(cursor.lastrowid) #aqui a tabela tem auto_increment, entao o id vem do banco
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                raise ValueError(
                    "Categoria ou filme da sequência não existe.") \
                    from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def listar_todos(self) -> list[Filme]:
        sql = ("SELECT idFilme, titulo, duracao_min, ano_lancamento, "
               "Categoria_idCategoria, Filme_idFilme_sequencia, disponivel "
               "FROM Filme "
               "ORDER BY titulo ASC")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Filme(**row) for row in rows]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_id(self, id_filme: int) -> Optional[Filme]:
        sql = ("SELECT idFilme, titulo, duracao_min, ano_lancamento, "
               "Categoria_idCategoria, Filme_idFilme_sequencia, disponivel "
               "FROM Filme "
               "WHERE idFilme = %s")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (id_filme,))
            row = cursor.fetchone()
            if not row:
                return None
            return Filme(**row)
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar(self, filme: Filme) -> bool:
        if filme.idFilme is None: #aqui eh is none, porque id 0 nao existe mas o not pegaria o zero
            raise ValueError("idFilme é obrigatório para atualizar um filme.")
        sql = ("UPDATE Filme SET titulo = %s, duracao_min = %s, ano_lancamento = %s, "
               "Categoria_idCategoria = %s, Filme_idFilme_sequencia = %s, "
               "disponivel = %s WHERE idFilme = %s")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (filme.titulo, filme.duracao_min,
                                 filme.ano_lancamento, filme.Categoria_idCategoria,
                                 filme.Filme_idFilme_sequencia, filme.disponivel,
                                 filme.idFilme))
            conn.commit()
            return cursor.rowcount > 0
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                raise ValueError(
                    "Categoria ou filme da sequência não existe.") \
                    from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def remover(self, id_filme: int) -> bool:
        sql = "DELETE FROM Filme WHERE idFilme = %s"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (id_filme,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_ROW_IS_REFERENCED_2:
                raise ValueError(
                    "Esse filme está em alguma locação e não pode ser removido.") \
                    from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()