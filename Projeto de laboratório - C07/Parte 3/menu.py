from mysql.connector import Error
from cliente_repository import Cliente, ClienteRepository


def _ler_texto(prompt: str) -> str:
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("Entrada vazia. Tente novamente.")


def _ler_int(prompt: str) -> int:
    while True:
        bruto = input(prompt).strip()
        try:
            return int(bruto)
        except ValueError:
            print("Digite um número inteiro válido.")


def executar_menu(repo: ClienteRepository) -> None:
    while True:
        print("\n=== MENU CLIENTES (MYSQL) ===")
        print("1. Cadastrar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por ID")
        print("4. Atualizar cliente")
        print("5. Remover cliente")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                nome = _ler_texto("Nome: ")
                cidade = _ler_texto("Cidade: ")
                novo_id = repo.criar(Cliente(id=None, nome=nome, cidade=cidade))
                print(f"Cliente cadastrado com ID {novo_id}.")

            elif opcao == "2":
                clientes = repo.listar_todos()
                if not clientes:
                    print("Nenhum cliente encontrado.")
                else:
                    print("\nID | Nome | Cidade")
                    for c in clientes:
                        print(f"{c.id} | {c.nome} | {c.cidade}")

            elif opcao == "3":
                cliente_id = _ler_int("ID do cliente: ")
                cliente = repo.buscar_por_id(cliente_id)
                if cliente:
                    print(f"Encontrado: [{cliente.id}] {cliente.nome} - {cliente.cidade}")
                else:
                    print("Cliente não encontrado.")

            elif opcao == "4":
                cliente_id = _ler_int("ID do cliente para atualizar: ")
                atual = repo.buscar_por_id(cliente_id)
                if not atual:
                    print("Cliente não encontrado.")
                    continue
                nome = _ler_texto(f"Novo nome [{atual.nome}]: ")
                cidade = _ler_texto(f"Nova cidade [{atual.cidade}]: ")
                ok = repo.atualizar(Cliente(id=cliente_id, nome=nome, cidade=cidade))
                print("Atualizado com sucesso." if ok else "Nenhuma alteração feita.")

            elif opcao == "5":
                cliente_id = _ler_int("ID do cliente para remover: ")
                ok = repo.remover(cliente_id)
                print("Removido com sucesso." if ok else "Cliente não encontrado.")

            elif opcao == "0":
                print("Encerrando...")
                break

            else:
                print("Opção inválida.")

        except Error as e:
            print(f"Erro no banco de dados: {e}")