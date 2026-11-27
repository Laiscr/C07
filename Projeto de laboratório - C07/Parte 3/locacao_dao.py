from dataclasses import dataclass
from datetime import date
from typing import Optional

from mysql.connector import Error, errorcode

from conexao import get_conexao


@dataclass
class Locacao:
    idLocacao: Optional[int]
    data_locacao: date
    data_prev_devolucao: date
    Cliente_cpf: str
    Funcionario_idFuncionario: int


class LocacaoDAO:
    def criar(self, locacao: Locacao) -> int:
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Locacao "
                "(data_locacao, data_prev_devolucao, Cliente_cpf, "
                "Funcionario_idFuncionario) VALUES (%s, %s, %s, %s)",
                (locacao.data_locacao, locacao.data_prev_devolucao,
                 locacao.Cliente_cpf, locacao.Funcionario_idFuncionario),
            )
            conn.commit()
            return int(cursor.lastrowid)
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                raise ValueError("O cliente ou funcionário informado não existe.") from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def listar_todos(self) -> list[Locacao]:
        sql = (
            "SELECT idLocacao, data_locacao, data_prev_devolucao, "
            "Cliente_cpf, Funcionario_idFuncionario "
            "FROM Locacao ORDER BY data_locacao DESC, idLocacao DESC"
        )
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return [Locacao(**row) for row in cursor.fetchall()]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_id(self, id_locacao: int) -> Optional[Locacao]:
        sql = (
            "SELECT idLocacao, data_locacao, data_prev_devolucao, "
            "Cliente_cpf, Funcionario_idFuncionario "
            "FROM Locacao WHERE idLocacao = %s"
        )
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (id_locacao,))
            row = cursor.fetchone()
            return Locacao(**row) if row else None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_cpf_cliente(self, cpf: str) -> list[Locacao]:
        sql = (
            "SELECT idLocacao, data_locacao, data_prev_devolucao, "
            "Cliente_cpf, Funcionario_idFuncionario "
            "FROM Locacao WHERE Cliente_cpf = %s "
            "ORDER BY data_locacao DESC, idLocacao DESC"
        )
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (cpf,))
            return [Locacao(**row) for row in cursor.fetchall()]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar(self, locacao: Locacao) -> bool:
        if locacao.idLocacao is None:
            raise ValueError("ID é obrigatório para atualizar uma locação.")
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Locacao SET data_locacao = %s, data_prev_devolucao = %s, "
                "Cliente_cpf = %s, Funcionario_idFuncionario = %s "
                "WHERE idLocacao = %s",
                (locacao.data_locacao, locacao.data_prev_devolucao,
                 locacao.Cliente_cpf, locacao.Funcionario_idFuncionario,
                 locacao.idLocacao),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                raise ValueError("O cliente ou funcionário informado não existe.") from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def remover(self, id_locacao: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Locacao WHERE idLocacao = %s", (id_locacao,))
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
