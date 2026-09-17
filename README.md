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

