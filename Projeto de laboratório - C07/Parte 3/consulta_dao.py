from mysql.connector import Error
from conexao import get_conexao


class ConsultaDAO:
    def _executar(self, sql: str) -> list[dict]:
        """Roda um SELECT sem parâmetros e devolve as linhas como dicionários."""
        conn = None
        cursor = None
        try:
            conn = get_conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def locacoes_com_devolucao(self) -> list[dict]:
        """Join 1:1 - cada locacao tem no maximo uma devolucao."""
        sql = (
            "SELECT locacao.idLocacao AS locacao, "
            "cliente.nome AS cliente, "
            "locacao.data_prev_devolucao AS prazo, "
            "devolucao.data_devolucao AS devolvido_em, "
            "devolucao.valor_multa AS multa "
            "FROM Locacao locacao "
            "INNER JOIN Cliente cliente "
            "    ON locacao.Cliente_cpf = cliente.cpf "
            "LEFT JOIN Devolucao devolucao "
            "    ON locacao.idLocacao = devolucao.Locacao_idLocacao "
            "ORDER BY locacao.idLocacao"
        )
        return self._executar(sql)

    def clientes_com_telefones(self) -> list[dict]:
        """Join 1:N - um cliente pode ter vários telefones."""
        sql = (
            "SELECT cliente.nome AS cliente, "
            "cliente.cidade AS cidade, "
            "telefone.telefone AS telefone "
            "FROM Cliente cliente "
            "INNER JOIN Telefone_Cliente telefone "
            "    ON cliente.cpf = telefone.Cliente_cpf "
            "ORDER BY cliente.nome, telefone.telefone"
        )
        return self._executar(sql)

    def filmes_com_atores(self) -> list[dict]:
        """Join N:M - a ligação passa pela tabela Atuação."""
        sql = (
            "SELECT filme.titulo AS filme, "
            "filme.ano_lancamento AS ano, "
            "ator.nome AS ator, "
            "atuacao.papel AS papel "
            "FROM Filme filme "
            "INNER JOIN Atuacao atuacao "
            "    ON filme.idFilme = atuacao.Filme_idFilme "
            "INNER JOIN Ator ator "
            "    ON atuacao.Ator_idAtor = ator.idAtor "
            "ORDER BY filme.titulo, ator.nome"
        )
        return self._executar(sql)