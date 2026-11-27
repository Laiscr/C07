from dataclasses import dataclass #gera automaticamente __init__, __repr__ e __eq__ para Categoria
from typing import Optional
from mysql.connector import Error, errorcode
from conexao import get_conexao

@dataclass
class Categoria:
    idCategoria: Optional[int]
    faixa_etaria: str

class CategoriaDAO:
    def criar(self, categoria: Categoria) -> int:
        sql = "INSERT INTO Categoria (faixa_etaria) VALUES (%s)"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (categoria.faixa_etaria,))
            conn.commit()
            return int(cursor.lastrowid) #a tabela tem auto_increment, então o id vem do banco
        except Error:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def listar_todos(self) -> list[Categoria]:
        sql = ("SELECT idCategoria, faixa_etaria "
               "FROM Categoria "
               "ORDER BY idCategoria ASC")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Categoria(**row) for row in rows]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_id(self, id_categoria: int) -> Optional[Categoria]:
        sql = ("SELECT idCategoria, faixa_etaria "
               "FROM Categoria "
               "WHERE idCategoria = %s")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (id_categoria,))
            row = cursor.fetchone()
            if not row:
                return None
            return Categoria(**row)
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_faixa_etaria(self, faixa_etaria: str) -> list[Categoria]:
        sql = ("SELECT idCategoria, faixa_etaria "
               "FROM Categoria "
               "WHERE faixa_etaria LIKE %s "
               "ORDER BY idCategoria ASC")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (f"%{faixa_etaria}%",))
            return [Categoria(**row) for row in cursor.fetchall()]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar(self, categoria: Categoria) -> bool:
        if categoria.idCategoria is None: #is None, porque o not pegaria o zero tambem
            raise ValueError("idCategoria é obrigatório para atualizar uma categoria.")
        sql = "UPDATE Categoria SET faixa_etaria = %s WHERE idCategoria = %s"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (categoria.faixa_etaria, categoria.idCategoria))
            conn.commit()
            return cursor.rowcount > 0
        except Error:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def remover(self, id_categoria: int) -> bool:
        sql = "DELETE FROM Categoria WHERE idCategoria = %s"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (id_categoria,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_ROW_IS_REFERENCED_2:
                raise ValueError("Essa categoria tem filmes cadastrados e não pode ser removida.") \
                    from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()