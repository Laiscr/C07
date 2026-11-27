from cliente_dao import ClienteDAO
from filme_dao import FilmeDAO
from categoria_dao import CategoriaDAO
from funcionario_dao import FuncionarioDAO
from locacao_dao import LocacaoDAO
from consulta_dao import ConsultaDAO
from menu import executar_menu

def main() -> None:
    cliente_dao = ClienteDAO()
    filme_dao = FilmeDAO()
    categoria_dao = CategoriaDAO()
    funcionario_dao = FuncionarioDAO()
    locacao_dao = LocacaoDAO()
    consulta_dao = ConsultaDAO()
    executar_menu(cliente_dao, filme_dao, categoria_dao,
                   funcionario_dao, locacao_dao, consulta_dao)

if __name__ == "__main__":
    main()