from cliente_dao import ClienteDAO
from filme_dao import FilmeDAO
from categoria_dao import CategoriaDAO
from menu import executar_menu

def main() -> None:
    cliente_dao = ClienteDAO()
    filme_dao = FilmeDAO()
    categoria_dao = CategoriaDAO()
    executar_menu(cliente_dao, filme_dao, categoria_dao)

if __name__ == "__main__":
    main()