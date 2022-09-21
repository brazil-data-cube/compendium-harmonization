..
    This file is part of Brazil Data Cube compendium-harmonization.
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


*[RC]: Research Compendium

# Processamento de dados

!!! info

    Este é um Capítulo de aplicação do material disponível neste RC. Caso você deseje explorar os conceitos por trás dos materiais e as formas de uso dos mesmos, por favor, consulte o Capítulo de [Referência do Compendium](/tools/).

A produção dos resultados apresentados no artigo associado a este RC, fez o uso de uma grande coleção de dados de Observação da terra (`~2TB`). Com esse grande volume de dados, atividades de gerenciamento e processamento desses dados pode exigir recursos que nem sempre estão disponíveis aos pesquisadores e interessados. De forma direta e indireta, isso faz com que ações de `verificação`, `validação`, `reprodução` e `replicação` dos materiais disponibilizados sejam problemáticas e trabalhosas de serem realizadas.

Para resolver esse problema e permitir que todos possam explorar os materiais que desenvolvemos, de modo a entender a implementação, organização e técnicas utilizadas, fez-se a criação de exemplos de utilização. Nesses exemplos, todos os materiais disponibilizados no RC são utilizados em conjunto para a construção do fluxo de processamento do trabalho. Os dados utilizados nesses exemplos, são *subsets* do conjunto de dados original utilizado na produção dos resultados do artigo. Também são utilizados conjuntos de dados não aplicados no artigo, para testar a possibilidade de replicação dos materiais deste RC.

Os exemplos disponíveis, são generalizáveis e podem ser utilizados como base para a `reprodução` do artigo e também a `replicação`, sendo necessário para essas ações, a troca do conjunto de dados de entrada.

!!! important "Exemplos generalizáveis e customizáveis"

    Essas características foram atribuídas aos exemplos disponibilizados já que, durante o desenvolvimento do artigo, eles foram os primeiros componentes a serem desenvolvidos. Em seguida, com as ferramentas prontas e testadas, fez-se a geração dos resultados finais.

    Para essa geração dos resultados finais, a única ação necessária foi a troca do conjunto de dados de entrada dos exemplos para o conjunto completo de dados do artigo. Com isso, é possível dizer que os exemplos são generalizábeis em seu uso e customizáveis o suficiente para permitir que outros conjuntos de dados e regiões sejam processados.


## Fluxo de operação dos exemplos

Ao todo, estão disponíveis dois exemplos com o uso dos materiais deste RC:

`Exemplo mínimo`

:   Exemplo de processamento completo, com todas as etapas da metodologia apresentada no artigo. Para esse exemplo, faz-se o uso de um pequeno *subset* de dados, retirados do conjunto de dados completo utilizado no artigo.

`Exemplo de replicação`

:   Seguindo exatamente os mesmos passos disponíveis no `Exemplo mínimo`, neste exemplo, faz-se o uso de um conjunto de dados de uma região não trabalhada no artigo original, para mostrar a possibilidade de replicação do fluxo de processamento implementado.

A realização de ambos os exemplos é feita seguindo os mesmos passos. Esses, conforme ilustrado na figura abaixo são divididos em três partes: `Download dos dados`; `Processamento (Jupyter)`; `Processamento (Dagster)`

<figure markdown>
  ![Examples flow](/assets/reproducible-research/minimal-example/examples-flow.svg){ width="1024" }
  <figcaption>Fluxo de operação dos exemplos</figcaption>
</figure>

No `Download de dados`, faz-se o *download* dos dados necessário para a execução do exemplo. Esses dados são disponibilizados através do [GitHub Release Assets](/pt/tools/utilitary/#example-toolkit). Em seguida, com os dados disponíveis, eles podem ser utilizados como entrada para o fluxo de processamento. Esse fluxo de processamento, está implementado em [duas tecnologias diferentes](/pt/tools/processing/), `Jupyter Notebook` e `Dagster`. Qualquer uma das implementações leva aos mesmos resultados. A diferença está no tipo de ambiente disponibilizado pelas ferramentas. Com o Jupyter Notebook, tem-se uma experiência interativa na execução das etapas de processamento, enquanto que no Dagster a operação ocorre em modo *batch*.

A realização dessas etapas, conforme será mostrado nas seções a seguir, é feita através de Docker Composes. Cada parte apresentada possui um Docker Compose específico, para que, essas, sejam realizadas de forma independente e num ambiente isolado. Neste caso, apenas os dados são compartilhado entre as partes.

## Automação

Conforme apresentado na Subseção anterior, para cada etapa realizada nos exemplos, tem-se um Docker Compose exclusivo. No entanto, ao utilizar essa estratégia, está sendo controlado apenas a recriação dos ambientes e as execuções. O uso desses Composes ainda é algo que deve ser realizado pelos usuários.

A realização dessas execuções pelo usuário não é um problema. Pode ser feito sem grandes dificuldades. No entanto, quando testes estão sendo feitos, tem-se operações de configuração de cada etapa que podem ser muito repetitivas. Para evitar essas repetições e os possíveis erros que essa ação pode causar, toda a lógica necessária para a execução de cada etapa, através do Docker Compose, foi colocada em um `Makefile`.

Com esse `Makefile`, os conjuntos de comandos necessários para a execução de cada etapa são abstraídos a simples execuções do [GNU Make](https://www.gnu.org/software/make/).

!!! tip "Make e pesquisa reprodutível"

    A ideia da utilização do `Make` foi retirada do magnífico [*The Turing Way handbook to reproducible, ethical and collaborative data science*](https://the-turing-way.netlify.app/welcome.html).

    Para mais sobre o `GNU Make` e pesquisa reprodutível, consulte o material [Reproducibility with Make](https://the-turing-way.netlify.app/reproducible-research/make.html).

Ao fazer o uso do `GNU Make`, conforme ilustrado na Figura abaixo, a interação com o Docker Compose e possíveis configurações necessárias nessas etapas, são realizadas através de códigos prontos e testados. Com isso, evitamos que erros nos comandos impessam o uso de nosso material. Além disso, por se tratar de um documento de texto simples, para aqueles que desejam obter cada etapa realizada, basta abrir o arquivo e verificar o que é realizado.

<figure markdown>
  ![Examples flow](/assets/reproducible-research/minimal-example/examples-flow-make.svg){ width="1024" }
  <figcaption>Fluxo de operação dos exemplos com Make</figcaption>
</figure>

Sendo assim, nos exemplos, será feito o uso do `GNU Make` junto ao `Makefile` para que as etapas de configuração sejam automatizadas, tornando o uso dos materiais mais simples e diretos.

#### Referência dos comandos disponíveis no Makefile

Para facilitar a utilização dos comandos disponíveis no `Makefile`, essa Subseção possui uma referência para cada um dos comandos disponíveis. Esses comandos, estão divididos em dois grupos: `Example` e `Replication`.

Os comandos `Example`, são aqueles que facilitam as operações para o `Exemplo mínimo`. Já os comandos `Replication` facilitam o exemplo de replicação. Desses grupos, deve-se notar que eles executam os mesmos comandos, os mesmos ambientes, trocando apenas os dados de entrada. Sendo assim, caso você deseje adaptar os códigos para seus dados, esses comados podem ser utilizados. Alternativamente, os arquivos Docker Compose utilizados pelo `Makefile` também estão disponíveis e podem ser modificados.

Nos tópicos abaixo, serão apresentados os comandos que estão disponíveis para cada um desses grupos:

**Example**

<div align="center" markdown>
|       **Comando**       |                             **Descrição**                            |
|:-----------------------:|:--------------------------------------------------------------------:|
| `example_cleanup_data`  | Remove todos os dados (Entrada e saída) utilizados no Exemplo mínimo |
| `example_download_data` | Realiza o download dos dados utilizados no Exemplo mínimo.           |
| `example_pipeline`      | Cria Container para a execução do Exemplo mínimo com Dagster         |
| `example_notebook`      | Cria Container para execução do Exemplo mínimo com Jupyter Notebook  |
</div>

**Replication**

<div align="center" markdown>
|          **Comando**         |                                **Descrição**                                |
|:----------------------------:|:---------------------------------------------------------------------------:|
| `replication_cleanup_data`   | Remove todos os dados (Entrada e saída) utilizados no Exemplo de replicação |
| `replication_ download_data` | Realiza o download dos dados utilizados no Exemplo de replicação            |
| `replication_pipeline`       | Cria Container para a execução do Exemplo de replicação com Dagster         |
| `replication_notebook`       | Cria Container para execução do Exemplo de replicação com Jupyter Notebook  |
</div>

Como pode-se notar, os comandos para ambos os exemplos são os mesmos. A mudança ocorre apenas na nomenclatura. Com relação ao funcionamento, como mencionado anteriormente, as operações são as mesmas, variando apenas nos dados de entrada que são utilizados.

## Pré-requisitos

Antes de iniciar os exemplos, certique-se que de que possui todas as ferramentas necessárias instaladas e configuradas em seu ambiente de trabalho. Abaixo, essas ferramentas são listadas e descritas:

[Git](https://git-scm.com/)

:   Sistema de controle de versões (Documentação criada com git versão `2.25.1`. Versões posteriores devem suportar os comandos utilizados);

[Docker](https://www.docker.com/)

:   Software de virtualização baseado em Containers (Documentação criada com Docker versão `0.10.12`. Versões posteriores devem suportar os comandos utilizados);

[Docker Compose](https://docs.docker.com/compose/)

:   Ferramenta para a orquestração e gerenciamento de Docker Containers (Documentação criada com Docker Compose versão `1.29.2`. Versões posteriores devem suportar os comandos utilizados).

[GNU Make](https://www.gnu.org/software/make/)

:   Ferramenta de automatização e controle de fluxos de *build* e execução (Documentação criada com `GNU Make` versão `4.2.1`. Versões posteriores devem suportar os comandos utilizados).

Caso você não tenha alguma dessas ferramentas, utilize os *links* acima para acessar as respectivas documentações oficiais e realizar as instalações necessárias.

!!! note "Sistema operacional"

    O sistema operacional utilizado para a criação de todos os materiais deste RC, foi o Ubuntu 20.04. Assim, é esperado que os passos apresentados, possam ser realizados em outras distros ou sistemas equivalentes (e.g., [MacOS](https://www.apple.com/br/macos/monterey/), [FreeBSD](https://www.freebsd.org/), [openSUSE](https://www.opensuse.org/)). Para Windows, pode ser que adaptações sejam necessárias.

    Caso você esteja utilizando o Windows e não deseja fazer modificações para utilizar o conteúdo deste RC, nós disponibilizados uma Máquina Virtual que pode ser utilizada. Para saber mais, por favor, consulte a Seção [Ambientes computacionais - Máquina virtual com Vagrant](/pt/tools/environment/#maquina-virtual-com-vagrant).


Após a instalação e configuração de todas as ferramentas listadas acima, você está pronto para iniciar os exemplos.
