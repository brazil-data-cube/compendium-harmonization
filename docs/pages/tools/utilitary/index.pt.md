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

<!-- ToDo: Modificar esse trecho para colocar o repositório oficial e os diretórios onde cada ferramenta mencionada está disponível -->

# Scripts auxiliares

A construção e publicação deste RC foi realizada em diversas etapas. Em cada etapa, além dos códigos que fazem a geração dos resultados propriamente ditos, foram desenvolvidos também diversos *scripts* auxiliares. Nesta seção, faz-se a apresentação desses *scripts*, seus detalhes de uso e forma de configuração.

### Calculate Checksum e GitHub Asset Upload

Para o compartilhamento deste RC, foi adotada uma estratégia em que todos os materiais que formam a versão completa do RC, foram organizados em um repositório do GitHub. Nesse repositório, tem-se todo o histórico de modificações realizadas nos materiais, códigos, documentação e os dados.

O armazenamento de materiais como os *scripts* e a documentação não requerem muito espaço em disco. Com isso, o uso do GitHub foi feito diretamente, sem a necessidade de modificações. No entanto, os dados auxiliares, que são utilizadas nos exemplos de execução e replicação disponíveis neste RC, possuem tamanhos que os tornam inviáveis para versionamento em repositórios git comum. Como alternativa, adotou-se a abordagem da publicação desses dados através dos [Release Assets](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). Com essa alternativa, arquivos com até 2 GB podem ser publicados e mantidos associados no repositório.

Com isso, fez-se necessário a preparação e organização dos dados, de modo que eles pudessem ser compartilhados no GitHub Release Assets. Para essa preparação, fez-se a criação de dois *scripts* auxiliares:

`Calculate Checksum`

:   `Calculate Checksum` é um *script* Python que realiza a criação de [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) e faz seu armazenamento em arquivos `zip`.

`GitHub Asset Upload`

:   Uma vez que os [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) são criados, o *script* R `GitHub Asset Upload` faz o envio desses arquivos para os servidores do GitHub. O processo é feito com o auxílio do pacote [piggyback](https://github.com/ropensci/piggyback).

Tendo como base esses dois pacotes, no repositório onde foram armazenados os *scripts* e a documentação, também pode-se disponibilizar os dados.

### Example toolkit

Conforme apresentado na seção anterior, os dados disponibilizados junto a este RC, foram publicados utilizando o [GitHub Release Assets](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). Para isso, são criados [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) dos dados em arquivos no formato `zip`. Esses, por sua vez, são armazenados nos servidores do GitHub.

Com essa estratégia, todos tem acesso aos dados e podem fazer seu uso para executar os exemplos disponibilizados neste RC. No entanto, para que os exemplos disponíveis neste RC possam ser utilizados, é necessário que os dados estejam organizados nos [diretórios corretos do RC](/pt/#organizacao-do-research-compendium).

Para resolver esse problema, e evitar o *download* e organização manual desses dados na estrutura do RC, fez-se a criação de um *script* Python, o `Example toolkit`. Com essa ferramenta, toda as etapas de *download* e organização são completamente automatizadas, sendo necessário para o usuário, apenas definir os diretórios que devem ser considerados no momento do *download*.

#### Operação

Ao realizar a utilização do `Example toolkit`, o *script* fará a execução de quatro etapas principais. Cada uma dessas etapas são representadas na figura abaixo:

<figure markdown>
  ![libs-link](/assets/tools/utilitary/example-toolkit/operation-flow.svg){ width="1024" }
  <figcaption>Fluxo de operação do Example Toolkit</figcaption>
</figure>

Conforme pode ser visto na figura acima, inicialmente, o `Example toolkit` realiza o *download* dos dados associados ao RC que estão armazenados no [GitHub Release Assets](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). Em seguida, para garantir que os dados baixados não sofreram mudanças ou estão corrompidos, é feita a validação do BagIts baixados, estrutura na qual os arquivos estão salvos. Após a validação, a ferramenta faz a extração dos dados para os diretórios corretos. Por fim, com base nas definições do usuário e onde os dados foram salvos, o `Example toolkit` faz a geração de um [arquivo de configuração Dagster](/pt/tools/processing/#arquivo-de-configuracao-dagster) que pode ser utilizado para iniciar o processamento dos dados baixados.


!!! info "Dagster e arquivo de configuração"

    Caso você deseje saber mais sobre como o Dagster é utilizado neste RC e onde o arquivo de configuração deve ser utilizado, consulte a Seção [Scripts de processamento - Dagster](/pt/tools/processing/#arquivo-de-configuracao-dagster).

Na próxima seção, é feita a apresentação de como o `Example toolkit` é configurado e executado.

#### Utilização

<!-- ToDo: Atualizar o link do diretório toolkit no github -->

Por se tratar de um *script* Python, a utilização do `Example toolkit`, requer apenas que você tenha o ambiente Python com as devidas dependências configuradas. Com o ambiente pronto, o código pode ser utilizado.

!!! tip "Example toolkit com Docker"

    Para utilizar o `Example toolkit` sem realizar nenhuma configuração de ambiente, consulte a seção [Example toolkit environment](/pt/tools/environment/#example-toolkit-environment) para mais explicações de como você pode utilizar a versão em Docker do script.

!!! tip "Configuração manual do ambiente"

    Para realizar a configuração manual do ambiente Python junto as dependências necessárias a utilização do `Example toolkit`, você pode utilizar o [conda](https://docs.conda.io/en/latest/). Com esse gerenciador de pacote, você pode criar um novo ambiente que possui todas as dependências exigidas pelo `Example toolkit`. Para criar esse ambiente, utilize o arquivo `environment.yml` que está disponível no diretório [tools/example-toolkit](#):

    ``` shell
    conda env create -f environment.yml
    ```

A primeira etapa necessária para a execução do `Example toolkit` é a definição das configurações que devem ser consideradas. Essas configurações, serão utilizadas para determinar o local onde os dados baixados serão salvos. São definidos também alguns parâmetros que auxiliam o *script* na geração do arquivo de configuração Dagster. A definição dessas configurações é feita através de variáveis de ambiente. Ao todo, as seguintes variáveis de ambiente devem ser declaradas:

<!-- ToDo: Atualizar o link do Exemplo mínimo e replicação para o github -->

`DOWNLOAD_REFERENCE_FILE`

:   Variável de ambiente para determinar o caminho absoluto para o arquivo `JSON` que define o endereço dos dados que serão baixados do GitHub Assets Release. Exemplos desse arquivo podem ser encontrados no diretório [tools/example-toolkit/config](#) deste RC.
:   *Exemplo de valor*: `/compendium/config/example-toolkit.json`

`DOWNLOAD_OUTPUT_DIRECTORY`

:   Variável de ambiente para determinar o diretório onde os dados baixados devem ser armazenados. Os dados serão organizados no formato do [Diretório de dados](/pt/tools/processing/#diretorio-de-dados), requerido pelos *scripts* de processamento deste RC.
:   *Exemplo de valor*: `/compendium/data`

`PIPELINE_DIR` (Configuração Dagster)

:   Variável de ambiente para determinar o diretório onde o arquivo de configuração do Dagster será salvo.
:   *Exemplo de valor*: `/compendium/config/config.yml`

`RAW_DATA_DIR` (Configuração Dagster)

:   Variável de ambiente para determinar o diretório da máquina que deve ser considerado o [input dir](#) do processamento Dagster.
:   *Exemplo de valor*: `/compendium/data/raw_data`

`DERIVED_DATA_DIR` (Configuração Dagster)

:   Variável de ambiente para determinar o diretório da máquina que deve ser considerado o [output dir](#) no arquivo de configuração Dagster.
:   *Exemplo de valor*: `/compendium/data/derived_data`

!!! note "Consistência de definição das variáveis"

    Deve-se notar que as variáveis de configuração possuem uma dependência lógica que deve ser seguida para que nenhum problema seja gerado. Para apresentar essa dependência, vamos considerar o exemplo abaixo:

    Supondo que você queira fazer o *download* dos dados no diretório `/opt/my-data`. Neste caso, você definirá a variável `DOWNLOAD_OUTPUT_DIRECTORY` da seguinte forma:

    ``` sh
    DOWNLOAD_OUTPUT_DIRECTORY=/opt/my-data
    ```

    Sabendo que os dados serão organizados seguindo o padrão de [Diretório de dados](/pt/tools/processing/#diretorio-de-dados), os dados baixados serão armazenados guardado da seguinte forma:

    ```
    /opt/my-data
        ├── derived_data
        └── raw_data
    ```

    Considerando essa organização, caso você queira que o arquivo de configuração Dagster seja gerado para processar os dados no diretório `/opt/my-data`, será necessário definir as variáveis de ambiente associadas a configuração do Dagster da seguinte forma:

    ``` sh
    # 1. Input dir
    RAW_DATA_DIR=/opt/my-data/raw_data

    # 2. Output dir
    DERIVED_DATA_DIR=/opt/my-data/derived_data
    ```

Feita a definição de cada uma dessas variáveis de ambiente, o `Example toolkit` pode ser executado. Para isso, o *script* disponível no diretório [tools/example-toolkit/scripts/pipeline.py](#) deve ser executado. Considerando que você está no diretório raiz deste RC, a execução desse *script* pode ser feita da seguinte forma:

*1. Mudando o diretório*

``` sh
cd tools/example-toolkit/
```

*2. Execução*

``` sh
python3 scripts/pipeline.py
```

Ao final da execução, tem-se como resultado nos diretórios de saída, os seguintes conteúdos:

**Dados**

O diretório definido na variável `DOWNLOAD_OUTPUT_DIRECTORY`, como mencionado, seguirá a organização do [Diretório de dados](/pt/tools/processing/#diretorio-de-dados) exigido pelos *scripts* de processamento deste RC. Assim, os dados estarão organizados da seguinte forma:

```
DOWNLOAD_OUTPUT_DIRECTORY
    ├── derived_data
    └── raw_data
        ├── landsat8_data
        ├── sentinel2_data
        ├── scene_id_list
        └── lasrc_auxiliary_data
```

**Configuração do Dagster**

O diretório definido na variável `PIPELINE_DIR` será populado com um [arquivo de configuração Dagster](/pt/tools/processing/#arquivo-de-configuracao-dagster) nomeado `config.yaml`. Neste arquivo, o seguinte conteúdo estará disponível:

``` yaml title="config.yaml: Arquivo de configuração Dagster"
resources:
  lasrc_data:
    config:
      lasrc_auxiliary_data_dir: {RAW_DATA_DIR}/lasrc_auxiliary_data
  repository:
    config:
      derived_data_dir: {DERIVED_DATA_DIR}
      landsat8_input_dir: {RAW_DATA_DIR}/landsat8_data
      sentinel2_input_dir: {RAW_DATA_DIR}/sentinel2_data
solids:
  load_and_standardize_sceneids_input:
    config:
      landsat8_sceneid_list:  {RAW_DATA_DIR}/scene_id_list/l8-sceneids.txt
      sentinel2_sceneid_list: {RAW_DATA_DIR}/scene_id_list/s2-sceneids.txt
```

Para um exemplo de uso completo e funcional do `Example toolkit`, consulte a seção [Pesquisa reprodutível - Exemplo mínimo](/pt/reproducible-research/minimal-example/).
