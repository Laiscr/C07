from dataclasses import dataclass #gera automaticamente __init__, __repr__ e __eq__ para Cliente
from mysql.connector import Error
from conexao import get_conexao


@dataclass
class Cliente:
    id: Optional[int]
    nome: str
    cidade: str


class ClienteRepository:
    def criar(self, cliente: Cliente) -> int:
        sql = "INSERT INTO Cliente (nome, cidade) VALUES (%s, %s)"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (cliente.nome, cliente.cidade))
            conn.commit()
            return int(cursor.lastrowid)
        except Error:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def listar_todos(self) -> list[Cliente]:
        sql = "SELECT id, nome, cidade FROM Cliente ORDER BY nome ASC"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                Cliente(id=row["id"], nome=row["nome"], cidade=row["cidade"])
                for row in rows
            ]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        sql = "SELECT id, nome, cidade FROM Cliente WHERE id = %s"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (cliente_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Cliente(id=row["id"], nome=row["nome"], cidade=row["cidade"])
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar(self, cliente: Cliente) -> bool:
        if cliente.id is None:
            raise ValueError("ID é obrigatório para atualizar um cliente.")
        sql = "UPDATE Cliente SET nome = %s, cidade = %s WHERE id = %s"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (cliente.nome, cliente.cidade, cliente.id))
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

    def remover(self, cliente_id: int) -> bool:
        sql = "DELETE FROM Cliente WHERE id = %s"
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (cliente_id,))
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