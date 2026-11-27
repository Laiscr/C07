# C07-Projeto_de_Laboratorio

## Locadora de Filmes

### Integrantes do Grupo
* **Nome do Integrante 1:** Laís Carlos Rodrigues - 681
* **Nome do Integrante 2:** Pedro Gasparotto Carvalho - 655

---

## Como funciona o projeto

Escolhemos criar um sistema para gerenciar uma **Locadora de Filmes**. Para ficar bem organizado e fácil de entender, nós dividimos o nosso banco de dados em 3 partes principais:

1. **Cadastro de Pessoas (Bloco Vermelho):** É onde salvamos as informações dos clientes e dos funcionários. Para os clientes, criamos uma tabela separada só para os telefones, assim eles podem ter mais de um número cadastrado. Para os funcionários, usamos uma regra de herança: todo mundo fica na tabela principal, mas separamos quem é `Atendente` e quem é `Gerente` em tabelas específicas, já que cada cargo tem funções diferentes na locadora.

2. **Catálogo de Filmes (Bloco Amarelo):** Aqui fica toda a nossa lista de filmes, organizados por suas respectivas categorias e classificações indicativas. Colocamos um relacionamento recursivo na tabela de filmes para conseguir cadastrar quando um filme é a sequência de outro (por exemplo, no caso de uma trilogia). Se o filme for único e não tiver sequência, esse campo simplesmente fica como NULL. Também criamos a tabela intermediária `Atuacao` para conectar os atores aos filmes, já que um ator pode trabalhar em vários filmes e um filme costuma ter vários atores.

3. **Operações de Locação (Bloco Verde):** Essa é a parte que controla quando um cliente faz um aluguel (`Locacao`) e quando ele realiza a entrega (`Devolucao`), registrando também os valores de multas caso ocorra algum atraso. Como um cliente pode alugar vários filmes de uma vez só na mesma visita, criamos a tabela intermediária `Posse` para listar quais filmes pertencem a qual locação. Além disso, mapeamos a devolução como uma entidade fraca, já que ela depende totalmente da existência de uma locação prévia para existir.

---

## Planejamento no Draw.io

Antes de passar o modelo para o MySQL Workbench, nós estruturamos toda a lógica conceitual no Draw.io seguindo as orientações que o professor Jonas passou nas aulas. 

Um detalhe importante é que a nomenclatura das chaves estrangeiras (FKs) ficou um pouco diferente entre as duas ferramentas. No Workbench, optamos por deixar os nomes que o próprio programa gera automaticamente para facilitar a legibilidade do diagrama. Já no desenho e tabelas do Draw.io, preferimos manter os nomes como aprendemos a fazer no mapeamento manual em sala de aula, por uma questão didática e de fixação do conteúdo. Todo o projeto foi desenvolvido exclusivamente pelos integrantes do grupo, sem o uso de inteligência artificial.

Caso queira ver também o arquivo original que fizemos no Draw.io, segue o link do nosso projeto:
[Locadora de Filmes](https://drive.google.com/file/d/1_A8rId83eSyD0cK5IDbRph6oz25M2ESa/view?usp=sharing)

# Parte 2
## Correção da Parte 1

O comentário recebido foi sobre tipo de dado. Os atributos com caractere especial viraram string:

| Atributo | Antes | Agora |
|---|---|---|
| cpf (Cliente e Funcionario) | INT | CHAR(15) |
| cep | INT | CHAR(9) |
| telefone | INT | CHAR(15) |
| ano_lancamento | DATE | CHAR(4) |

Pelo mesmo motivo, os campos de dinheiro (salario, valor_multa e limite_desc_multa) saíram de FLOAT e INT e foram para DECIMAL(10,2), que não come os centavos. O resto do modelo ficou igual.

---

## Estrutura

13 tabelas: as 12 do modelo mais a `Log_Locacao`, criada como extra para a auditoria.

| Tipo | Onde |
|---|---|
| 1:1 | Locacao com Devolucao |
| 1:N | Cliente com Telefone_Cliente, Cliente com Locacao, Funcionario com Locacao, Categoria com Filme |
| N:M | Ator com Filme (via Atuacao), Locacao com Filme (via Posse) |
| Autorrelacionamento | Filme aponta para Filme, nas continuações |
| Herança | Funcionario para Funcionario_Atendente e Funcionario_Gerente |

A herança usa uma tabela por subclasse. A chave primária da subclasse também é chave estrangeira para Funcionario, o que garante o 1:1 e evita coluna nula. No bloco DQL tem uma consulta que traz as duas subclasses juntas: quem é atendente aparece com turno e limite nulo, quem é gerente aparece ao contrário.

---

## Onde está cada requisito

| Pedido | Onde no script |
|---|---|
| Banco e tabelas do modelo | Bloco DDL |
| 5 registros por tabela | Bloco de inserção, confirmado pelos COUNT no final. |
| DML com o motivo explicado | Bloco de manipulação, 4 UPDATE e 2 DELETE comentados. |
| Herança igual ao modelo | Funcionario_Atendente e Funcionario_Gerente |
| Dois usuários por uma ROLE | Bloco DCL, `lais_atendente` e `pedro_atendente` na role `atendente_locadora`. |
| JOIN com 1:1, 1:N e N:M | Bloco DQL, a 1ª consulta é o 1:1, a 2ª é o 1:N e a 4ª é o N:M. |
| Procedure, View, Trigger e Function | Bloco de objetos programáveis. |
| Extras documentados | Abaixo. |

O bloco DQL tem sete consultas no total. Além das três obrigatórias, tem uma com GROUP BY, uma que junta os três relacionamentos de uma vez, uma com as duas subclasses da herança e uma com subquery.
Obs: os blocos são identificados, seus inícios, por estarem dentro de linhas tracejadas para facilitar. Comentados. É bom relevar.

---

## Os quatro objetos programáveis

Foram feitos em cima da mesma regra, a multa por atraso, para um usar o outro:

| Objeto | O que faz | Por que esse tipo |
|---|---|---|
| `fn_calcular_multa` | R$ 2,50 por dia de atraso. | function só calcula e devolve valor, então pode ser chamada dentro de um SELECT, e a regra fica guardada num lugar só. |
| `trg_devolucao_calcula_multa` | Preenche a multa em todo INSERT na Devolucao | trigger para não depender de alguém lembrar de calcular, e BEFORE porque mexe no valor antes de gravar. |
| `sp_registrar_devolucao` | Confere se a locação existe, se já não foi devolvida e se a data bate, e só então insere | procedure porque executa INSERT, coisa que function não faz. |
| `vw_locacoes_detalhadas` | Consulta pronta com os vários JOINs | view para não reescrever a consulta toda hora, e esconde coluna como o salário. |

---

## Extras

| Item | O que é |
|---|---|
| TCL | START TRANSACTION, SAVEPOINT, ROLLBACK TO e COMMIT ao prorrogar duas locações, onde só a segunda é desfeita. |
| Segundo trigger | `trg_locacao_auditoria`, AFTER INSERT, que alimenta a `Log_Locacao` sozinho. |
| Auditoria | Tabela `Log_Locacao`, que nunca recebe INSERT direto. |
| Índice | `idx_locacao_prazo` na data de devolução prevista, seguido de uma consulta que filtra e ordena por essa coluna. |
| ALTER TABLE | Coluna `disponivel` com ENUM, adicionada sem perder os dados. |
| Autorrelacionamento | Filme ligado a ele mesmo, com consulta própria mostrando as continuações. |

---

## Contagem final

| Tabela | Registros |
|---|---|
| Cliente | 5 |
| Telefone_Cliente | 5 |
| Funcionario | 10 |
| Funcionario_Atendente | 5 |
| Funcionario_Gerente | 5 |
| Categoria | 6 |
| Ator | 5 |
| Filme | 8 |
| Atuacao | 8 |
| Locacao | 11 |
| Posse | 14 |
| Devolucao | 5 |
| Log_Locacao | 5 |

Algumas tabelas começam com mais e terminam com menos por causa dos DELETE de demonstração. Outras crescem no meio do script, com o teste do trigger e com a procedure. Os COUNT no fim do arquivo mostram esses números.

### Materiais de apoio
* Slides das aulas de laboratório
* [C07 - Gemini](https://share.gemini.google/mYUAVWOlzP42)
* [Documentação do MySQL](https://dev.mysql.com/doc/refman/8.0/en/create-table.html)

# Parte 3 - Integração com Python

A aplicação é um programa de terminal escrito em Python, usando o conector oficial
`mysql-connector-python`. O SQL fica isolado em arquivos DAO, um por entidade, e o
`main.py` só monta os objetos e chama o menu.

### Como executar

Pré-requisitos: Python 3.10 ou superior e o MySQL rodando na máquina.

1. Rode o script `Parte 2/Parte 2.sql` no MySQL Workbench. Ele apaga e recria o banco
   `locadora_filmes` do zero, já com os dados de teste. A aplicação não cria tabela
   nenhuma, só usa o que está lá.

2. Crie e ative o ambiente virtual, a partir da raiz do repositório:

   ```
   python -m venv .venv
   .venv\Scripts\activate       (Windows)
   source .venv/bin/activate    (Linux/macOS)
   ```

3. Instale a dependência:

   ```
   pip install -r requirements.txt
   ```

4. Ajuste as credenciais, se as suas forem diferentes de `root`/`root`. O `conexao.py`
   lê de variáveis de ambiente, então não é preciso editar o arquivo:

   ```
   set DB_PASSWORD=suasenha       (Windows)
   export DB_PASSWORD=suasenha    (Linux/macOS)
   ```

   As variáveis aceitas são `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` e `DB_NAME`.
   Sem nenhuma delas, valem os padrões: localhost, 3306, root, root, locadora_filmes.

5. Execute a aplicação:

   ```
   python "Parte 3/main.py"
   ```

Para testar só a conexão, sem abrir o menu, rode `python "Parte 3/conexao.py"`. Ele
imprime a versão do servidor e lista os clientes.

### Arquivos

| Arquivo | O que faz |
|---|---|
| `conexao.py` | Centraliza host, porta, usuário, senha e banco. Todo DAO importa o `get_conexao()` daqui |
| `cliente_dao.py` | CRUD de Cliente |
| `filme_dao.py` | CRUD de Filme |
| `categoria_dao.py` | CRUD de Categoria |
| `funcionario_dao.py` | CRUD de Funcionário, incluindo as subclasses Atendente e Gerente |
| `locacao_dao.py` | CRUD de Locação |
| `consulta_dao.py` | As consultas com join e a leitura da view |
| `devolucao_dao.py` | Registro de devolução, chamando a procedure da Parte 2 |
| `menu.py` | Menu principal e submenus |
| `main.py` | Ponto de entrada |

### O menu

O menu principal dá acesso a cinco entidades e a um submenu de consultas. Cada submenu
de entidade tem cadastro, listagem geral, busca por chave, busca por atributo,
atualização e remoção.

O cadastro de funcionário pede o cargo e grava a tabela `Funcionario` junto com a
tabela da subclasse correspondente na mesma transação, com rollback se qualquer um dos
dois INSERT falhar. As locações referenciam o CPF de um cliente e o ID de um
funcionário já cadastrados.

Além da busca pela chave primária, há buscas por cidade do cliente, título do filme,
faixa etária da categoria, CPF do funcionário e CPF do cliente nas locações. As buscas
por cidade, título e faixa etária aceitam correspondência parcial.

### Onde está cada requisito

| Requisito | Onde |
|---|---|
| Menu interativo com CRUD | `menu.py`, cinco submenus de entidade |
| 5 entidades gerenciáveis | Cliente, Filme, Categoria, Funcionário e Locação |
| Busca geral | `listar_todos()` em cada DAO |
| Busca por filtro | `buscar_por_cpf`, `buscar_por_id`, `buscar_por_cidade`, `buscar_por_titulo`, `buscar_por_faixa_etaria`, `buscar_por_cpf_cliente` |
| Update com filtro | `atualizar()` em cada DAO, com WHERE na chave primária |
| Update sem filtro | `atualizar_disponibilidade_todos()` em `filme_dao.py`, um UPDATE sem WHERE, e `reajustar_salario_atendentes()` em `funcionario_dao.py`, que atinge o grupo inteiro por subquery. Os dois pedem confirmação antes de executar |
| Delete com filtro | `remover()` em cada DAO, sempre com WHERE na chave primária. Não existe caminho no programa que apague em massa |
| Join 1:1 | Locação com Devolução, submenu Consultas opção 1 |
| Join 1:N | Cliente com Telefone_Cliente, opção 2 |
| Join N:M | Filme com Ator via Atuação, opção 3 |

### Uso dos objetos da Parte 2

A aplicação não refaz no Python o que já estava resolvido no banco:

* A opção 4 do submenu Consultas lê a view `vw_locacoes_detalhadas` em vez de repetir
  os cinco joins. A view também protege as tabelas, porque quem consulta ela não
  enxerga o salário do funcionário.
* A opção 7 do submenu Locações chama a procedure `sp_registrar_devolucao` com
  `callproc`. As três validações (locação existe, ainda não foi devolvida, data
  coerente) acontecem dentro da procedure, e a multa é calculada pela trigger
  `trg_devolucao_calcula_multa`, que usa a function `fn_calcular_multa`. O Python só
  envia o ID e a data.

### Tratamento de erros

Toda query usa parâmetros `%s`, nunca concatenação, o que fecha a porta para SQL
injection. Os erros do banco são traduzidos antes de chegar à tela:

| Código | Quando acontece | Mensagem |
|---|---|---|
| 1451 | Apagar um registro que ainda é referenciado | "Esse cliente tem locações registradas e não pode ser removido", e equivalentes para filme, categoria e funcionário |
| 1452 | Cadastrar apontando para um pai inexistente | "Categoria ou filme da sequência não existe" |
| 1062 | Violação de UNIQUE | "Já existe um funcionário com esse CPF" |

### Materiais de apoio
* Slides das aulas de laboratório
* [Laís - Gemini](https://share.gemini.google/Nj10vbdq1Bhe)
* [Google for Education - Python](https://developers.google.com/edu/python?hl=pt-br)
* [Python - Glossary](https://docs.python.org/pt-br/3/glossary.html)
