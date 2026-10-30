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

