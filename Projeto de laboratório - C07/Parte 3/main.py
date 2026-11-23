from cliente_repository import ClienteRepository
from menu import executar_menu


def main() -> None:
    repo = ClienteRepository()
    executar_menu(repo)


if __name__ == "__main__":
    main()