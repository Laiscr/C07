from mysql.connector import Error
from cliente_dao import Cliente, ClienteDAO


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


def executar_menu(repo: ClienteDAO) -> None:
    while True:
        print("\n=== MENU CLIENTES (MYSQL) ===")
        print("1. Cadastrar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por CPF")
        print("4. Atualizar cliente")
        print("5. Remover cliente")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cpf = _ler_texto("CPF (000.000.000-00): ")
                nome = _ler_texto("Nome: ")
                rua = _ler_texto("Rua: ")
                numero_casa = _ler_int("Número: ")
                bairro = _ler_texto("Bairro: ")
                cep = _ler_texto("CEP (00000-000): ")
                cidade = _ler_texto("Cidade: ")
                novo_cpf = repo.criar(Cliente(cpf=cpf, nome=nome, rua=rua,
                                              numero_casa=numero_casa, bairro=bairro,
                                              cep=cep, cidade=cidade))
                print(f"Cliente cadastrado com CPF {novo_cpf}.")

            elif opcao == "2":
                clientes = repo.listar_todos()
                if not clientes:
                    print("Nenhum cliente encontrado.")
                else:
                    print(f"\n{'CPF':<16} | {'NOME':<25} | CIDADE")
                    for c in clientes:
                        print(f"{c.cpf:<16} | {c.nome:<25} | {c.cidade}")

            elif opcao == "3":
                cpf = _ler_texto("CPF do cliente: ")
                cliente = repo.buscar_por_cpf(cpf)
                if cliente:
                    print(f"Encontrado: [{cliente.cpf}] {cliente.nome} - "
                          f"{cliente.rua}, {cliente.numero_casa} - {cliente.cidade}")
                else:
                    print("Cliente não encontrado.")

            elif opcao == "4":
                cpf = _ler_texto("CPF do cliente para atualizar: ")
                atual = repo.buscar_por_cpf(cpf)
                if not atual:
                    print("Cliente não encontrado.")
                    continue
                nome = _ler_texto(f"Novo nome [{atual.nome}]: ")
                rua = _ler_texto(f"Nova rua [{atual.rua}]: ")
                numero_casa = _ler_int(f"Novo número [{atual.numero_casa}]: ")
                bairro = _ler_texto(f"Novo bairro [{atual.bairro}]: ")
                cep = _ler_texto(f"Novo CEP [{atual.cep}]: ")
                cidade = _ler_texto(f"Nova cidade [{atual.cidade}]: ")
                ok = repo.atualizar(Cliente(cpf=cpf, nome=nome, rua=rua,
                                            numero_casa=numero_casa, bairro=bairro,
                                            cep=cep, cidade=cidade))
                print("Atualizado com sucesso." if ok else "Nenhuma alteração feita.")

            elif opcao == "5":
                cpf = _ler_texto("CPF do cliente para remover: ")
                ok = repo.remover(cpf)
                print("Removido com sucesso." if ok else "Cliente não encontrado.")

            elif opcao == "0":
                print("Encerrando...")
                break

            else:
                print("Opção inválida.")

        except ValueError as e:
            print(f"Operação recusada: {e}")

        except Error as e:
            print(f"Erro no banco de dados: {e}")