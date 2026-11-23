# conexao.py
#centraliza o acesso ao banco de dados MySQL.
#nenhum outro arquivo do projeto repete host, usuario ou senha (de acordo com o material).

import mysql.connector

CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "locadora_filmes",
}


def get_conexao():
    """Tenta estabelecer e retornar uma conexao com o MySQL."""
    return mysql.connector.connect(**CONFIG)


if __name__ == "__main__":
    conexao = get_conexao()
    print("Conectado:", conexao.is_connected())
    print("Servidor:", conexao.server_info)

    cursor = conexao.cursor()
    cursor.execute("SELECT DATABASE()")
    print("Banco em uso:", cursor.fetchone()[0])

    cursor.execute("SELECT nome, cidade FROM Cliente ORDER BY nome")
    for nome, cidade in cursor.fetchall():
        print(f"  {nome} - {cidade}")

    cursor.close()
    conexao.close()
    print("Conectado:", conexao.is_connected())