from mysql.connector import Error
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Optional
from cliente_dao import Cliente, ClienteDAO
from filme_dao import Filme, FilmeDAO
from categoria_dao import Categoria, CategoriaDAO
from funcionario_dao import Funcionario, FuncionarioDAO
from locacao_dao import Locacao, LocacaoDAO
from consulta_dao import ConsultaDAO


def _ler_texto(prompt: str, padrao: Optional[str] = None) -> str:
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        if padrao is not None:
            return padrao
        print("Entrada vazia. Tente novamente.")


def _ler_int(prompt: str, padrao: Optional[int] = None) -> int:
    while True:
        bruto = input(prompt).strip()
        if not bruto and padrao is not None:
            return padrao
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


def _ler_data(prompt: str, padrao: Optional[date] = None) -> date:
    while True:
        bruto = input(prompt).strip()
        if not bruto and padrao is not None:
            return padrao
        try:
            return datetime.strptime(bruto, "%Y-%m-%d").date()
        except ValueError:
            print("Digite uma data válida no formato AAAA-MM-DD.")


def _ler_decimal(prompt: str, padrao: Optional[Decimal] = None) -> Decimal:
    while True:
        bruto = input(prompt).strip().replace(",", ".")
        if not bruto and padrao is not None:
            return padrao
        try:
            return Decimal(bruto)
        except InvalidOperation:
            print("Digite um valor numérico válido.")


def _ler_cargo(prompt: str, padrao: Optional[str] = None) -> str:
    while True:
        valor = input(prompt).strip().capitalize()
        if not valor and padrao:
            return padrao
        if valor in ("Atendente", "Gerente"):
            return valor
        print("Digite Atendente ou Gerente.")


def _ler_disponivel(prompt: str) -> str:
    while True:
        valor = input(prompt).strip().capitalize()
        if valor in ("Sim", "Nao", "Não"):
            return "Nao" \
                if valor.startswith("N") \
                else "Sim"
        print("Responda apenas Sim ou Nao.")


def executar_menu(cliente_dao: ClienteDAO, filme_dao: FilmeDAO,
                  categoria_dao: CategoriaDAO, funcionario_dao: FuncionarioDAO,
                  locacao_dao: LocacaoDAO, consulta_dao: ConsultaDAO) -> None:
    while True:
        print("\n===== LOCADORA DE FILMES =====")
        print("1. Clientes")
        print("2. Filmes")
        print("3. Categorias")
        print("4. Funcionários")
        print("5. Locações")
        print("6. Consultas")
        print("7. Reajustar salário de todos os atendentes")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            _menu_clientes(cliente_dao)
        elif opcao == "2":
            _menu_filmes(filme_dao)
        elif opcao == "3":
            _menu_categorias(categoria_dao)
        elif opcao == "4":
            _menu_funcionarios(funcionario_dao)
        elif opcao == "5":
            _menu_locacoes(locacao_dao)
        elif opcao == "6":
            _menu_consultas(consulta_dao)
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
        print("4. Buscar clientes por cidade")
        print("5. Atualizar cliente")
        print("6. Remover cliente")
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
                cidade = _ler_texto("Cidade para buscar: ")
                clientes = cliente_dao.buscar_por_cidade(cidade)
                if not clientes:
                    print("Nenhum cliente encontrado nessa cidade.")
                else:
                    print(f"\n{'CPF':<16} | {'NOME':<25} | CIDADE")
                    for c in clientes:
                        print(f"{c.cpf:<16} | {c.nome:<25} | {c.cidade}")

            elif opcao == "5":
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

            elif opcao == "6":
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

def _menu_funcionarios(dao: FuncionarioDAO) -> None:
    while True:
        print("\n=== MENU FUNCIONÁRIOS ===")
        print("1. Cadastrar funcionário")
        print("2. Listar funcionários")
        print("3. Buscar funcionário por ID")
        print("4. Buscar funcionário por CPF")
        print("5. Atualizar funcionário")
        print("6. Remover funcionário")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()
        try:
            if opcao == "1":
                cargo = _ler_cargo("Cargo (Atendente/Gerente): ")
                nome = _ler_texto("Nome: ")
                data_nascimento = _ler_data("Data de nascimento (AAAA-MM-DD): ")
                cpf = _ler_texto("CPF (000.000.000-00): ")
                salario = _ler_decimal("Salário: ")
                turno = _ler_texto("Turno: ") if cargo == "Atendente" else None
                limite = _ler_decimal("Limite de desconto de multa: ") \
                    if cargo == "Gerente" else None
                funcionario = Funcionario(
                    idFuncionario=None, nome=nome, data_nascimento=data_nascimento,
                    cpf=cpf, salario=salario, cargo=cargo, turno=turno,
                    limite_desc_multa=limite)
                novo_id = dao.criar(funcionario)
                print(f"Funcionário {cargo.lower()} cadastrado com ID {novo_id}.")

            elif opcao == "2":
                funcionarios = dao.listar_todos()
                if not funcionarios:
                    print("Nenhum funcionário encontrado.")
                else:
                    print(f"\n{'ID':<4} | {'NOME':<25} | {'CPF':<16} | "
                          f"{'CARGO':<10} | DETALHE")
                    print("-" * 85)
                    for f in funcionarios:
                        detalhe = f"Turno: {f.turno}" if f.cargo == "Atendente" \
                            else f"Limite multa: {f.limite_desc_multa}"
                        print(f"{f.idFuncionario:<4} | {f.nome:<25} | {f.cpf:<16} | "
                              f"{f.cargo:<10} | {detalhe}")

            elif opcao == "3":
                id_funcionario = _ler_int("ID do funcionário: ")
                funcionario = dao.buscar_por_id(id_funcionario)
                if funcionario:
                    _exibir_funcionario(funcionario)
                else:
                    print("Funcionário não encontrado.")

            elif opcao == "4":
                cpf = _ler_texto("CPF do funcionário: ")
                funcionario = dao.buscar_por_cpf(cpf)
                if funcionario:
                    _exibir_funcionario(funcionario)
                else:
                    print("Funcionário não encontrado.")

            elif opcao == "5":
                id_funcionario = _ler_int("ID do funcionário para atualizar: ")
                atual = dao.buscar_por_id(id_funcionario)
                if not atual:
                    print("Funcionário não encontrado.")
                    continue
                cargo = _ler_cargo(
                    f"Cargo (Atendente/Gerente) [{atual.cargo}]: ", atual.cargo)
                nome = _ler_texto(f"Novo nome [{atual.nome}]: ", atual.nome)
                data_nascimento = _ler_data(
                    f"Nova data de nascimento [{atual.data_nascimento}] "
                    "(AAAA-MM-DD): ", atual.data_nascimento)
                cpf = _ler_texto(f"Novo CPF [{atual.cpf}]: ", atual.cpf)
                salario = _ler_decimal(f"Novo salário [{atual.salario}]: ",
                                       atual.salario)
                turno = _ler_texto(
                    f"Novo turno [{atual.turno or ''}]: ", atual.turno) \
                    if cargo == "Atendente" else None
                limite = _ler_decimal(
                    f"Novo limite de desconto [{atual.limite_desc_multa or 0}]: ",
                    atual.limite_desc_multa or Decimal("0.00")) \
                    if cargo == "Gerente" else None
                ok = dao.atualizar(Funcionario(
                    idFuncionario=id_funcionario, nome=nome,
                    data_nascimento=data_nascimento, cpf=cpf, salario=salario,
                    cargo=cargo, turno=turno, limite_desc_multa=limite))
                print("Atualizado com sucesso." if ok else "Funcionário não encontrado.")

            elif opcao == "6":
                id_funcionario = _ler_int("ID do funcionário para remover: ")
                ok = dao.remover(id_funcionario)
                print("Removido com sucesso." if ok else "Funcionário não encontrado.")

            elif opcao == "7":
                percentual = _ler_decimal("Percentual de reajuste (ex.: 8): ")
                confirma = _ler_texto("Isso altera todos os atendentes. Confirma? (Sim/Nao): ")
                if confirma.strip().capitalize().startswith("S"):
                    afetados = dao.reajustar_salario_atendentes(percentual)
                    print(f"{afetados} atendente(s) reajustado(s).")
                else:
                    print("Operação cancelada.")

            elif opcao == "0":
                break
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Operação recusada: {e}")
        except Error as e:
            print(f"Erro no banco de dados: {e}")


def _exibir_funcionario(funcionario: Funcionario) -> None:
    print(f"ID: {funcionario.idFuncionario}")
    print(f"Nome: {funcionario.nome}")
    print(f"Data de nascimento: {funcionario.data_nascimento}")
    print(f"CPF: {funcionario.cpf}")
    print(f"Salário: {funcionario.salario}")
    print(f"Cargo: {funcionario.cargo}")
    if funcionario.cargo == "Atendente":
        print(f"Turno: {funcionario.turno}")
    else:
        print(f"Limite de desconto de multa: {funcionario.limite_desc_multa}")

# ==========================

def _menu_locacoes(dao: LocacaoDAO) -> None:
    while True:
        print("\n=== MENU LOCAÇÕES ===")
        print("1. Cadastrar locação")
        print("2. Listar locações")
        print("3. Buscar locação por ID")
        print("4. Buscar locações por CPF do cliente")
        print("5. Atualizar locação")
        print("6. Remover locação")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()
        try:
            if opcao == "1":
                locacao = Locacao(
                    idLocacao=None,
                    data_locacao=_ler_data("Data da locação (AAAA-MM-DD): "),
                    data_prev_devolucao=_ler_data(
                        "Data prevista para devolução (AAAA-MM-DD): "),
                    Cliente_cpf=_ler_texto("CPF do cliente: "),
                    Funcionario_idFuncionario=_ler_int("ID do funcionário: "),
                )
                novo_id = dao.criar(locacao)
                print(f"Locação cadastrada com ID {novo_id}.")

            elif opcao == "2":
                locacoes = dao.listar_todos()
                if not locacoes:
                    print("Nenhuma locação encontrada.")
                else:
                    print(f"\n{'ID':<4} | {'DATA':<10} | {'DEVOLUÇÃO':<10} | "
                          f"{'CPF CLIENTE':<16} | ID FUNCIONÁRIO")
                    print("-" * 70)
                    for l in locacoes:
                        print(f"{l.idLocacao:<4} | {l.data_locacao} | "
                              f"{l.data_prev_devolucao} | {l.Cliente_cpf:<16} | "
                              f"{l.Funcionario_idFuncionario}")

            elif opcao == "3":
                id_locacao = _ler_int("ID da locação: ")
                locacao = dao.buscar_por_id(id_locacao)
                if locacao:
                    _exibir_locacao(locacao)
                else:
                    print("Locação não encontrada.")

            elif opcao == "4":
                cpf = _ler_texto("CPF do cliente: ")
                locacoes = dao.buscar_por_cpf_cliente(cpf)
                if not locacoes:
                    print("Nenhuma locação encontrada para esse cliente.")
                else:
                    for locacao in locacoes:
                        print("-" * 40)
                        _exibir_locacao(locacao)

            elif opcao == "5":
                id_locacao = _ler_int("ID da locação para atualizar: ")
                atual = dao.buscar_por_id(id_locacao)
                if not atual:
                    print("Locação não encontrada.")
                    continue
                locacao = Locacao(
                    idLocacao=id_locacao,
                    data_locacao=_ler_data(
                        f"Nova data da locação [{atual.data_locacao}] "
                        "(AAAA-MM-DD): ", atual.data_locacao),
                    data_prev_devolucao=_ler_data(
                        f"Nova devolução prevista [{atual.data_prev_devolucao}] "
                        "(AAAA-MM-DD): ", atual.data_prev_devolucao),
                    Cliente_cpf=_ler_texto(
                        f"Novo CPF do cliente [{atual.Cliente_cpf}]: ",
                        atual.Cliente_cpf),
                    Funcionario_idFuncionario=_ler_int(
                        f"Novo ID do funcionário "
                        f"[{atual.Funcionario_idFuncionario}]: ",
                        atual.Funcionario_idFuncionario),
                )
                ok = dao.atualizar(locacao)
                print("Atualizada com sucesso." if ok else "Nenhuma alteração feita.")

            elif opcao == "6":
                id_locacao = _ler_int("ID da locação para remover: ")
                ok = dao.remover(id_locacao)
                print("Removida com sucesso." if ok else "Locação não encontrada.")

            elif opcao == "0":
                break
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Operação recusada: {e}")
        except Error as e:
            print(f"Erro no banco de dados: {e}")


def _exibir_locacao(locacao: Locacao) -> None:
    print(f"ID: {locacao.idLocacao}")
    print(f"Data da locação: {locacao.data_locacao}")
    print(f"Devolução prevista: {locacao.data_prev_devolucao}")
    print(f"CPF do cliente: {locacao.Cliente_cpf}")
    print(f"ID do funcionário: {locacao.Funcionario_idFuncionario}")

# ==========================

def _menu_filmes(dao: FilmeDAO) -> None:
    while True:
        print("\n=== MENU FILMES ===")
        print("1. Cadastrar filme")
        print("2. Listar filmes")
        print("3. Buscar filme por ID")
        print("4. Buscar filmes por título")
        print("5. Atualizar filme")
        print("6. Remover filme")
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
                titulo = _ler_texto("Título para buscar: ")
                filmes = dao.buscar_por_titulo(titulo)
                if not filmes:
                    print("Nenhum filme encontrado com esse título.")
                else:
                    print(f"\n{'ID':<4} | {'TÍTULO':<25} | {'ANO':<5} | "
                          f"{'MIN':<4} | DISPONÍVEL")
                    for f in filmes:
                        print(f"{f.idFilme:<4} | {f.titulo:<25} | "
                              f"{f.ano_lancamento:<5} | {f.duracao_min:<4} | "
                              f"{f.disponivel}")

            elif opcao == "5":
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

            elif opcao == "6":
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
        print("4. Buscar categorias por faixa etária")
        print("5. Atualizar categoria")
        print("6. Remover categoria")
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
                faixa_etaria = _ler_texto("Faixa etária para buscar: ")
                categorias = dao.buscar_por_faixa_etaria(faixa_etaria)
                if not categorias:
                    print("Nenhuma categoria encontrada com essa faixa etária.")
                else:
                    print(f"\n{'ID':<4} | Faixa etária")
                    print("-" * 30)
                    for c in categorias:
                        print(f"{c.idCategoria:<4} | {c.faixa_etaria}")

            elif opcao == "5":
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

            elif opcao == "6":
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

# ==========================

def _menu_consultas(dao: ConsultaDAO) -> None:
    while True:
        print("\n=== MENU CONSULTAS ===")
        print("1. Locações e devoluções (1:1)")
        print("2. Clientes e telefones (1:N)")
        print("3. Filmes e atores (N:M)")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                linhas = dao.locacoes_com_devolucao()
                if not linhas:
                    print("Nenhuma locação encontrada.")
                else:
                    print(f"\n{'LOC':<4} | {'CLIENTE':<22} | {'PRAZO':<10} | " f"{'DEVOLVIDO':<10} | MULTA")
                    print("-" * 70)
                    for l in linhas:
                        devolvido = (l["devolvido_em"].strftime("%d/%m/%Y")
                                     if l["devolvido_em"] else "em aberto")
                        multa = (f"R$ {l['multa']:.2f}"
                                 if l["multa"] is not None else "-")
                        print(f"{l['locacao']:<4} | {l['cliente']:<22} | " f"{l['prazo'].strftime('%d/%m/%Y'):<10} | " f"{devolvido:<10} | {multa}")

            elif opcao == "2":
                linhas = dao.clientes_com_telefones()
                if not linhas:
                    print("Nenhum telefone cadastrado.")
                else:
                    print(f"\n{'CLIENTE':<22} | {'CIDADE':<24} | TELEFONE")
                    print("-" * 70)
                    for l in linhas:
                        print(f"{l['cliente']:<22} | {l['cidade']:<24} | " f"{l['telefone']}")

            elif opcao == "3":
                linhas = dao.filmes_com_atores()
                if not linhas:
                    print("Nenhuma atuação cadastrada.")
                else:
                    print(f"\n{'FILME':<25} | {'ANO':<5} | {'ATOR':<20} | PAPEL")
                    print("-" * 70)
                    for l in linhas:
                        print(f"{l['filme']:<25} | {l['ano']:<5} | " f"{l['ator']:<20} | {l['papel']}")

            elif opcao == "0":
                break

            else:
                print("Opção inválida.")

        except Error as e:
            print(f"Erro no banco de dados: {e}")