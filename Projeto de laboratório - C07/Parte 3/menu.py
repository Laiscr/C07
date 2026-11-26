from mysql.connector import Error
from typing import Optional
from cliente_dao import Cliente, ClienteDAO
from filme_dao import Filme, FilmeDAO
from categoria_dao import Categoria, CategoriaDAO


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


def _ler_int_opcional(prompt: str) -> Optional[int]:
    """Devolve None quando a pessoa aperta enter sem digitar nada."""
    while True:
        bruto = input(prompt).strip()
        if not bruto:
            return None
        try:
            return int(bruto)
        except ValueError:
            print("Digite um número inteiro válido ou deixe em branco.")


def _ler_disponivel(prompt: str) -> str:
    while True:
        valor = input(prompt).strip().capitalize()
        if valor in ("Sim", "Nao", "Não"):
            return "Nao" \
                if valor.startswith("N") \
                else "Sim"
        print("Responda apenas Sim ou Nao.")


def executar_menu(cliente_dao: ClienteDAO, filme_dao: FilmeDAO, categoria_dao: CategoriaDAO) -> None:
    while True:
        print("\n===== LOCADORA DE FILMES =====")
        print("1. Clientes")
        print("2. Filmes")
        print("3. Categorias")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            _menu_clientes(cliente_dao)
        elif opcao == "2":
            _menu_filmes(filme_dao)
        elif opcao == "3":
            _menu_categorias(categoria_dao)
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


def _menu_clientes(cliente_dao: ClienteDAO) -> None:
    while True:
        print("\n=== MENU CLIENTES ===")
        print("1. Cadastrar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por CPF")
        print("4. Atualizar cliente")
        print("5. Remover cliente")
        print("0. Voltar")

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
                novo_cpf = cliente_dao.criar(Cliente(cpf=cpf, nome=nome, rua=rua,
                                                     numero_casa=numero_casa, bairro=bairro,
                                                     cep=cep, cidade=cidade))
                print(f"Cliente cadastrado com CPF {novo_cpf}.")

            elif opcao == "2":
                clientes = cliente_dao.listar_todos()
                if not clientes:
                    print("Nenhum cliente encontrado.")
                else:
                    print(f"\n{'CPF':<16} | {'NOME':<25} | CIDADE")
                    for c in clientes:
                        print(f"{c.cpf:<16} | {c.nome:<25} | {c.cidade}")

            elif opcao == "3":
                cpf = _ler_texto("CPF do cliente: ")
                cliente = cliente_dao.buscar_por_cpf(cpf)
                if cliente:
                    print(f"Encontrado: [{cliente.cpf}] {cliente.nome} - "
                          f"{cliente.rua}, {cliente.numero_casa} - {cliente.cidade}")
                else:
                    print("Cliente não encontrado.")

            elif opcao == "4":
                cpf = _ler_texto("CPF do cliente para atualizar: ")
                atual = cliente_dao.buscar_por_cpf(cpf)
                if not atual:
                    print("Cliente não encontrado.")
                    continue
                nome = _ler_texto(f"Novo nome [{atual.nome}]: ")
                rua = _ler_texto(f"Nova rua [{atual.rua}]: ")
                numero_casa = _ler_int(f"Novo número [{atual.numero_casa}]: ")
                bairro = _ler_texto(f"Novo bairro [{atual.bairro}]: ")
                cep = _ler_texto(f"Novo CEP [{atual.cep}]: ")
                cidade = _ler_texto(f"Nova cidade [{atual.cidade}]: ")
                ok = cliente_dao.atualizar(Cliente(cpf=cpf, nome=nome, rua=rua,
                                                   numero_casa=numero_casa, bairro=bairro,
                                                   cep=cep, cidade=cidade))
                print("Atualizado com sucesso."
                      if ok
                      else "Nenhuma alteração feita.")

            elif opcao == "5":
                cpf = _ler_texto("CPF do cliente para remover: ")
                ok = cliente_dao.remover(cpf)
                print("Removido com sucesso."
                      if ok
                      else "Cliente não encontrado.")

            elif opcao == "0":
                break

            else:
                print("Opção inválida.")

        except ValueError as e:
            print(f"Operação recusada: {e}")

        except Error as e:
            print(f"Erro no banco de dados: {e}")


# ==========================

def _menu_filmes(dao: FilmeDAO) -> None:
    while True:
        print("\n=== MENU FILMES ===")
        print("1. Cadastrar filme")
        print("2. Listar filmes")
        print("3. Buscar filme por ID")
        print("4. Atualizar filme")
        print("5. Remover filme")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                titulo = _ler_texto("Título: ")
                duracao_min = _ler_int("Duração em minutos: ")
                ano_lancamento = _ler_texto("Ano de lançamento (4 dígitos): ")
                categoria = _ler_int("ID da categoria: ")
                sequencia = _ler_int_opcional("ID do filme anterior da sequência (Enter se não houver): ")
                disponivel = _ler_disponivel("Disponível (Sim/Não): ")
                novo_id = dao.criar(Filme(idFilme=None, titulo=titulo,
                                          duracao_min=duracao_min,
                                          ano_lancamento=ano_lancamento,
                                          Categoria_idCategoria=categoria,
                                          Filme_idFilme_sequencia=sequencia,
                                          disponivel=disponivel))
                print(f"Filme cadastrado com ID {novo_id}.")

            elif opcao == "2":
                filmes = dao.listar_todos()
                if not filmes:
                    print("Nenhum filme encontrado.")
                else:
                    print(f"\n{'ID':<4} | {'TÍTULO':<25} | {'ANO':<5} | "
                          f"{'MIN':<4} | DISPONÍVEL")
                    print("-" * 60)
                    for f in filmes:
                        print(f"{f.idFilme:<4} | {f.titulo:<25} | "
                              f"{f.ano_lancamento:<5} | {f.duracao_min:<4} | "
                              f"{f.disponivel}")

            elif opcao == "3":
                id_filme = _ler_int("ID do filme: ")
                filme = dao.buscar_por_id(id_filme)
                if filme:
                    print(f"\nID: {filme.idFilme}")
                    print(f"Título: {filme.titulo}")
                    print(f"Duração: {filme.duracao_min} min")
                    print(f"Ano: {filme.ano_lancamento}")
                    print(f"Categoria: {filme.Categoria_idCategoria}")
                    print(f"Continuação de: {filme.Filme_idFilme_sequencia}")
                    print(f"Disponível: {filme.disponivel}")
                else:
                    print("Filme não encontrado.")

            elif opcao == "4":
                id_filme = _ler_int("ID do filme para atualizar: ")
                atual = dao.buscar_por_id(id_filme)
                if not atual:
                    print("Filme não encontrado.")
                    continue
                titulo = _ler_texto(f"Novo título [{atual.titulo}]: ")
                duracao_min = _ler_int(f"Nova duração [{atual.duracao_min}]: ")
                ano_lancamento = _ler_texto(f"Novo ano [{atual.ano_lancamento}]: ")
                categoria = _ler_int(f"Nova categoria [{atual.Categoria_idCategoria}]: ")
                sequencia = _ler_int_opcional(
                    f"Nova sequência [{atual.Filme_idFilme_sequencia}], " f"Enter para nenhuma: ")
                disponivel = _ler_disponivel(f"Disponível [{atual.disponivel}] (Sim/Nao): ")
                ok = dao.atualizar(Filme(idFilme=id_filme, titulo=titulo,
                                         duracao_min=duracao_min,
                                         ano_lancamento=ano_lancamento,
                                         Categoria_idCategoria=categoria,
                                         Filme_idFilme_sequencia=sequencia,
                                         disponivel=disponivel))
                print("Atualizado com sucesso."
                      if ok
                      else "Nenhuma alteração feita.")

            elif opcao == "5":
                id_filme = _ler_int("ID do filme para remover: ")
                ok = dao.remover(id_filme)
                print("Removido com sucesso."
                      if ok
                      else "Filme não encontrado.")

            elif opcao == "0":
                break

            else:
                print("Opção inválida.")

        except ValueError as e:
            print(f"Operação recusada: {e}")
        except Error as e:
            print(f"Erro no banco de dados: {e}")


# ===================

def _menu_categorias(dao: CategoriaDAO) -> None:
    while True:
        print("\n=== MENU CATEGORIAS ===")
        print("1. Cadastrar categoria")
        print("2. Listar categorias")
        print("3. Buscar categoria por ID")
        print("4. Atualizar categoria")
        print("5. Remover categoria")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                faixa_etaria = _ler_texto("Faixa etária (ex.: 12 anos): ")
                novo_id = dao.criar(Categoria(idCategoria=None,
                                              faixa_etaria=faixa_etaria))
                print(f"Categoria cadastrada com ID {novo_id}.")

            elif opcao == "2":
                categorias = dao.listar_todos()
                if not categorias:
                    print("Nenhuma categoria encontrada.")
                else:
                    print(f"\n{'ID':<4} | Faixa etária")
                    print("-" * 30)
                    for c in categorias:
                        print(f"{c.idCategoria:<4} | {c.faixa_etaria}")

            elif opcao == "3":
                id_categoria = _ler_int("ID da categoria: ")
                categoria = dao.buscar_por_id(id_categoria)
                if categoria:
                    print(f"Encontrada: [{categoria.idCategoria}] "
                          f"{categoria.faixa_etaria}")
                else:
                    print("Categoria não encontrada.")

            elif opcao == "4":
                id_categoria = _ler_int("ID da categoria para atualizar: ")
                atual = dao.buscar_por_id(id_categoria)
                if not atual:
                    print("Categoria não encontrada.")
                    continue
                faixa_etaria = _ler_texto(f"Nova faixa etária [{atual.faixa_etaria}]: ")
                ok = dao.atualizar(Categoria(idCategoria=id_categoria,
                                             faixa_etaria=faixa_etaria))
                print("Atualizada com sucesso."
                      if ok
                      else "Nenhuma alteração feita.")

            elif opcao == "5":
                id_categoria = _ler_int("ID da categoria para remover: ")
                ok = dao.remover(id_categoria)
                print("Removida com sucesso."
                      if ok
                      else "Categoria não encontrada.")

            elif opcao == "0":
                break

            else:
                print("Opção inválida.")

        except ValueError as e:
            print(f"Operação recusada: {e}")
        except Error as e:
            print(f"Erro no banco de dados: {e}")
