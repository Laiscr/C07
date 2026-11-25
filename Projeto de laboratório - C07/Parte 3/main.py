from cliente_dao import ClienteDAO
from menu import executar_menu


def main() -> None:
    repo = ClienteDAO()
    executar_menu(repo)


if __name__ == "__main__":
    main()