# conexao.py
#centraliza o acesso ao banco de dados MySQL.
#nenhum outro arquivo do projeto repete host, usuario ou senha (de acordo com o material).
import os
import mysql.connector

CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "locadora_filmes"),
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