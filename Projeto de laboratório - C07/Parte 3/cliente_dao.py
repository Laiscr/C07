from dataclasses import dataclass #gera automaticamente __init__, __repr__ e __eq__ para Cliente
from typing import Optional
from mysql.connector import Error, errorcode
from conexao import get_conexao


@dataclass
class Cliente:
    cpf: str
    nome: str
    rua: str
    numero_casa: int
    bairro: str
    cep: str
    cidade: str


class ClienteDAO:
    def criar(self, cliente: Cliente) -> str:
        sql = ("INSERT INTO Cliente (cpf, nome, rua, numero_casa, bairro, cep, cidade) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (cliente.cpf, cliente.nome, cliente.rua,
                                 cliente.numero_casa, cliente.bairro,
                                 cliente.cep, cliente.cidade))
            conn.commit()
            return cliente.cpf #o outro retorno usava do auto_increment da tabela do workbench, mas não tem auto_increment la
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
        sql = ("SELECT cpf, nome, rua, numero_casa, bairro, cep, cidade "
               "FROM Cliente "
               "ORDER BY nome ASC")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Cliente(**row) for row in rows]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        sql = ("SELECT cpf, nome, rua, numero_casa, bairro, cep, cidade "
               "FROM Cliente "
               "WHERE cpf = %s")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (cpf,))
            row = cursor.fetchone()
            if not row:
                return None
            return Cliente(**row)
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar(self, cliente: Cliente) -> bool:
        if not cliente.cpf: #not pega None e string vazia
            raise ValueError("CPF é obrigatório para atualizar um cliente.")
        sql = ("UPDATE Cliente SET nome = %s, rua = %s, numero_casa = %s, "
               "bairro = %s, cep = %s, cidade = %s WHERE cpf = %s")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (cliente.nome, cliente.rua, cliente.numero_casa,
                                 cliente.bairro, cliente.cep, cliente.cidade,
                                 cliente.cpf))
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

    def remover(self, cpf: str) -> bool:
        sql = ("DELETE FROM Cliente WHERE cpf = %s")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (cpf,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_ROW_IS_REFERENCED_2:
                raise ValueError(
                    "Esse cliente tem locações registradas e não pode ser removido.") \
                    from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()