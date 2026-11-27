from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from mysql.connector import Error, errorcode

from conexao import get_conexao


@dataclass
class Funcionario:
    idFuncionario: Optional[int]
    nome: str
    data_nascimento: date
    cpf: str
    salario: Decimal
    cargo: str
    turno: Optional[str] = None
    limite_desc_multa: Optional[Decimal] = None


class FuncionarioDAO:
    def _validar_subclasse(self, funcionario: Funcionario) -> None:
        if funcionario.cargo == "Atendente":
            if not funcionario.turno:
                raise ValueError("O turno é obrigatório para atendentes.")
        elif funcionario.cargo == "Gerente":
            if funcionario.limite_desc_multa is None:
                raise ValueError("O limite de desconto é obrigatório para gerentes.")
        else:
            raise ValueError("O cargo deve ser Atendente ou Gerente.")

    def criar(self, funcionario: Funcionario) -> int:
        self._validar_subclasse(funcionario)
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Funcionario (nome, data_nascimento, cpf, salario) "
                "VALUES (%s, %s, %s, %s)",
                (funcionario.nome, funcionario.data_nascimento,
                 funcionario.cpf, funcionario.salario),
            )
            id_funcionario = int(cursor.lastrowid)

            if funcionario.cargo == "Atendente":
                cursor.execute(
                    "INSERT INTO Funcionario_Atendente "
                    "(Funcionario_idFuncionario, turno) VALUES (%s, %s)",
                    (id_funcionario, funcionario.turno),
                )
            else:
                cursor.execute(
                    "INSERT INTO Funcionario_Gerente "
                    "(Funcionario_idFuncionario, limite_desc_multa) "
                    "VALUES (%s, %s)",
                    (id_funcionario, funcionario.limite_desc_multa),
                )

            conn.commit()
            return id_funcionario
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_DUP_ENTRY:
                raise ValueError("Já existe um funcionário com esse CPF.") from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def listar_todos(self) -> list[Funcionario]:
        sql = (
            "SELECT f.idFuncionario, f.nome, f.data_nascimento, f.cpf, f.salario, "
            "CASE WHEN fa.Funcionario_idFuncionario IS NOT NULL THEN 'Atendente' "
            "WHEN fg.Funcionario_idFuncionario IS NOT NULL THEN 'Gerente' "
            "ELSE 'Funcionario' END AS cargo, fa.turno, fg.limite_desc_multa "
            "FROM Funcionario f "
            "LEFT JOIN Funcionario_Atendente fa "
            "ON fa.Funcionario_idFuncionario = f.idFuncionario "
            "LEFT JOIN Funcionario_Gerente fg "
            "ON fg.Funcionario_idFuncionario = f.idFuncionario "
            "ORDER BY f.nome ASC"
        )
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return [Funcionario(**row) for row in cursor.fetchall()]
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        sql = (
            "SELECT f.idFuncionario, f.nome, f.data_nascimento, f.cpf, f.salario, "
            "CASE WHEN fa.Funcionario_idFuncionario IS NOT NULL THEN 'Atendente' "
            "WHEN fg.Funcionario_idFuncionario IS NOT NULL THEN 'Gerente' "
            "ELSE 'Funcionario' END AS cargo, fa.turno, fg.limite_desc_multa "
            "FROM Funcionario f "
            "LEFT JOIN Funcionario_Atendente fa "
            "ON fa.Funcionario_idFuncionario = f.idFuncionario "
            "LEFT JOIN Funcionario_Gerente fg "
            "ON fg.Funcionario_idFuncionario = f.idFuncionario "
            "WHERE f.idFuncionario = %s"
        )
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (id_funcionario,))
            row = cursor.fetchone()
            return Funcionario(**row) if row else None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_cpf(self, cpf: str) -> Optional[Funcionario]:
        sql = (
            "SELECT f.idFuncionario, f.nome, f.data_nascimento, f.cpf, f.salario, "
            "CASE WHEN fa.Funcionario_idFuncionario IS NOT NULL THEN 'Atendente' "
            "WHEN fg.Funcionario_idFuncionario IS NOT NULL THEN 'Gerente' "
            "ELSE 'Funcionario' END AS cargo, fa.turno, fg.limite_desc_multa "
            "FROM Funcionario f "
            "LEFT JOIN Funcionario_Atendente fa "
            "ON fa.Funcionario_idFuncionario = f.idFuncionario "
            "LEFT JOIN Funcionario_Gerente fg "
            "ON fg.Funcionario_idFuncionario = f.idFuncionario "
            "WHERE f.cpf = %s"
        )
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (cpf,))
            row = cursor.fetchone()
            return Funcionario(**row) if row else None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar(self, funcionario: Funcionario) -> bool:
        if funcionario.idFuncionario is None:
            raise ValueError("ID é obrigatório para atualizar um funcionário.")
        self._validar_subclasse(funcionario)
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT idFuncionario FROM Funcionario WHERE idFuncionario = %s",
                (funcionario.idFuncionario,),
            )
            if not cursor.fetchone():
                return False

            cursor.execute(
                "UPDATE Funcionario SET nome = %s, data_nascimento = %s, "
                "cpf = %s, salario = %s WHERE idFuncionario = %s",
                (funcionario.nome, funcionario.data_nascimento, funcionario.cpf,
                 funcionario.salario, funcionario.idFuncionario),
            )
            cursor.execute(
                "DELETE FROM Funcionario_Atendente "
                "WHERE Funcionario_idFuncionario = %s",
                (funcionario.idFuncionario,),
            )
            cursor.execute(
                "DELETE FROM Funcionario_Gerente "
                "WHERE Funcionario_idFuncionario = %s",
                (funcionario.idFuncionario,),
            )
            if funcionario.cargo == "Atendente":
                cursor.execute(
                    "INSERT INTO Funcionario_Atendente "
                    "(Funcionario_idFuncionario, turno) VALUES (%s, %s)",
                    (funcionario.idFuncionario, funcionario.turno),
                )
            else:
                cursor.execute(
                    "INSERT INTO Funcionario_Gerente "
                    "(Funcionario_idFuncionario, limite_desc_multa) "
                    "VALUES (%s, %s)",
                    (funcionario.idFuncionario, funcionario.limite_desc_multa),
                )
            conn.commit()
            return True
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_DUP_ENTRY:
                raise ValueError("Já existe um funcionário com esse CPF.") from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def reajustar_salario_atendentes(self, percentual: Decimal) -> int:
        """UPDATE em massa: reajusta de uma vez o salário de todos os atendentes."""
        sql = (
            "UPDATE Funcionario SET salario = salario * (1 + %s / 100) "
            "WHERE idFuncionario IN "  # ------------
            "(SELECT Funcionario_idFuncionario FROM Funcionario_Atendente)"
        )
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(sql, (percentual,))
            conn.commit()
            return cursor.rowcount
        except Error:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def remover(self, id_funcionario: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Funcionario WHERE idFuncionario = %s",
                (id_funcionario,),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Error as erro:
            if conn:
                conn.rollback()
            if erro.errno == errorcode.ER_ROW_IS_REFERENCED_2:
                raise ValueError(
                    "Esse funcionário está associado a locações e não pode ser removido."
                ) from erro
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
