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

# Exemplo mínimo

!!! attention "Pré-requisitos"

    Antes de iniciar esse exemplo, certifique-se de ter os [pré-requisitos](/pt/reproducible-research/#pre-requisitos) instalados em seu ambiente de trabalho.

Associado a este RC, está um artigo em que é realizado experimentos de harmonização entre satélites-sensores Landsat-8/OLI e Sentinel-2/MSI. Conforme apresentado no [Capítulo de Referência](/pt/tools/), os materiais e ferramentas deste RC, representam todo o esforço de desenvolvimento empregado para a geração dos resultados desse artigo.

Nesta Seção, faz-se a apresentação do uso desse material em um exemplo reprodutível de aplicação do fluxo de processamento desenvolvido no artigo para a geração de produtos de harmonização. Os dados utilizados são um pequeno *subset* de 4 cenas (`2x Landsat-8/OLI` e `2x Sentinel-2/MSI`) extraído do conjunto de dados original.

Espera-se que com esse exemplo, os pesquisadores e interessados sejam capazes de explorar os materiais produzidos e a forma de implementação do fluxo de processamento do artigo.

!!! tip "Referência"

    Esta é uma Seção prática, onde faz-se o uso dos materiais disponibilizados no RC. Caso seja necessário obter mais informações sobre as ferramentas utilizadas, por favor, consulte o [Capítulo de Referência](/pt/tools/).

## Download do Research Compendium

O primeiro passo para a realização desse exemplo, é o *download* deste RC e todos os seus materiais. Para isso, em um terminal, utilize a ferramenta `git` e faça o [clone](https://git-scm.com/docs/git-clone) do repositório onde o RC está armazenado:

``` sh
git clone https://github.com/brazil-data-cube/compendium-harmonization
```

Após o [clone](https://git-scm.com/docs/git-clone), um novo diretório será criado no diretório em que você está. O nome deste novo diretório é `compendium-harmonization`:

``` sh
ls -ls .

#> 4 drwxrwxr-x 3 ubuntu ubuntu 4096 May  2 00:44 compendium-harmonization
```

Agora, acesse o diretório `compendium-harmonization` e liste os conteúdos:

*Mudando de diretório*
``` sh
cd compendium-harmonization
```

*Listando o conteúdo do diretório*

``` sh
ls -ls .

#> total 76K
#> drwxrwxr-x 9 ubuntu ubuntu 4.0K May  1 23:29 .
#> drwxrwxr-x 4 ubuntu ubuntu 4.0K May  2 00:44 ..
#> drwxrwxr-x 5 ubuntu ubuntu 4.0K Apr 14 17:00 analysis
#> -rw-rw-r-- 1 ubuntu ubuntu 1.4K May  1 16:36 bootstrap.sh
#> drwxrwxr-x 4 ubuntu ubuntu 4.0K Apr 14 17:00 composes
#> drwxrwxr-x 4 ubuntu ubuntu 4.0K Apr 14 17:00 docker
#> -rw-rw-r-- 1 ubuntu ubuntu  375 May  1 16:36 .dockerignore
#> drwxrwxr-x 3 ubuntu ubuntu 4.0K May  1 16:44 docs
#> drwxrwxr-x 7 ubuntu ubuntu 4.0K Apr 14 17:00 .git
#> drwxrwxr-x 3 ubuntu ubuntu 4.0K Apr 15 22:53 .github
#> -rw-rw-r-- 1 ubuntu ubuntu 4.6K May  1 16:36 .gitignore
#> -rw-rw-r-- 1 ubuntu ubuntu 1.1K May  1 16:35 LICENSE
#> -rw-rw-r-- 1 ubuntu ubuntu 2.7K May  1 16:36 Makefile
#> -rw-rw-r-- 1 ubuntu ubuntu 4.5K Apr  9 20:01 README.md
#> -rw-rw-r-- 1 ubuntu ubuntu  392 May  1 16:36 setenv.sh
#> drwxrwxr-x 6 ubuntu ubuntu 4.0K Apr 14 17:00 tools
#> -rw-rw-r-- 1 ubuntu ubuntu 3.4K May  1 16:36 Vagrantfile
```

Como você pode observar, o conteúdo do diretório representa todos os materiais deste RC. Esse será o conteúdo base utilizado para a realização desse tutorial. A descrição de cada arquivo diretório deste RC pode ser encontrada na [Introdução](/pt/#organizacao-do-research-compendium) desta documentação.

## Download dos dados

Após o *download* do RC, seguindo as etapas apresentadas na introdução do Capítulo ([Processamento de dados](/pt/reproducible-research/#processamento-de-dados)), primeiro é necessário que seja feito o *download* dos dados que serão utilizados no exemplo. Esses dados, conforme especificado na Seção [Example Toolkit](/pt/tools/utilitary/#example-toolkit), são armazenados no [GitHub Release Assets](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

Sendo assim, será necessário utilizar o [Example Toolkit](/pt/tools/utilitary/#example-toolkit). Essa ferramenta, faz o *download* dos dados e os organiza na estrutura requerida pelos [scripts de processamento](/pt/tools/processing/#diretorio-de-dados) deste RC.

Para fazer essa execução, primeiro faça a criação da rede Docker a qual os Containers criados neste tutorial ficarão associados. Para isso, em seu terminal, utilize o seguinte comando:

``` sh
docker network create research_processing_network

#> fdaa46b4fe70bd34b6cb0e59734376234d801599a1fb1cbe1d9fd66a8f5044b1
```

Agora, através do `GNU Make`, faça a execução do comando `example_download_data`:

``` sh
make example_download_data
```

!!! tip "Pro tip"

    Na execução do `GNU Make`, caso você tenha algum problema de permissão relacionado a execução do arquivo `setenv.sh`, utilize o seguinte comando antes de executar o `GNU Make` novamente:

    ``` sh
    chmod +x setenv.sh
    ```

Esse comando, fará a utilização do Docker Compose específico para o *download* de dados deste exemplo. Ao executá-lo, o *download* dos dados será iniciado e uma mensagem parecida com a apresentada abaixo deverá ser exibida (Alguns campos foram omitidos do exemplo para torná-lo mais agradável de ser visualizado na documentação):

``` sh
Creating example-minimal-download-data ... done
Attaching to example-minimal-download-data
(omitted)    | 2022-05-02 01:16:20.078 | INFO     | (omitted) - Downloading minimal-example_landsat8_data.zip (omitted)
(omitted)    | 2022-05-02 01:21:09.345 | INFO     | (omitted) - Downloading minimal-example_lasrc_auxiliary_data.zip (omitted)
(omitted)    | 2022-05-02 01:22:35.845 | INFO     | (omitted) - Downloading minimal-example_scene_id_list.zip (omitted)
(omitted)    | 2022-05-02 01:22:36.510 | INFO     | (omitted) - Downloading minimal-example_sentinel2_data.zip (omitted)
(omitted)    | 2022-05-02 01:25:14.653 | INFO     | (omitted) - All files are downloaded.
example-minimal-download-data exited with code 0
```

!!! tip "Download dos dados"

    Caso você deseje obter mais informações sobre o processo de *download* dos dados, por favor, consulte a Seção de referência [Scripts auxiliares](/pt/tools/utilitary/#scripts-auxiliares).

Seguindo a [organização](#) do RC, os dados baixados foram armazenados no diretório `analysis/data/examples/minimal_example/raw_data/`:

``` sh
ls -ls analysis/data/examples/minimal_example/raw_data/

#> total 16
#> 4 drwxrwxrwx 4 root root 4096 May  2 01:25 landsat8_data
#> 4 drwxrwxrwx 5 root root 4096 May  2 01:22 lasrc_auxiliary_data
#> 4 drwxrwxrwx 2 root root 4096 May  2 01:22 scene_id_list
#> 4 drwxrwxrwx 4 root root 4096 May  2 01:25 sentinel2_data
```

!!! tip "Organização dos dados"

    A organização dos dados no diretório `analysis/data/examples/minimal_example/raw_data/`, seguem o padrão requerido pelos *scripts* de processamento. Para mais informações, por favor, consulte a Seção de referência [Diretório de dados](/pt/tools/processing/#diretorio-de-dados).


## Processando dados com Jupyter Notebook

Dando continuidade ao fluxo apresentado na [introdução do Capítulo](/pt/reproducible-research/), uma primeira forma de realizar a aplicação do processamento descrito no artigo associado a este RC, é através de um Jupyter Notebook. Esse documento, tem a descrição detalhada de cada uma das etapas do fluxo de processamento. Neste exemplo, os notebooks serão a primeira abordagem apresentada.

!!! tip "Jupyter Notebook em todo lugar"

    Para saber mais sobre os Jupyter Notebooks neste RC, consulte a Seção [Scripts de processamento - Jupyter Notebook](/pt/tools/processing/#jupyter-notebook).

Para fazer o uso dos notebooks e processar os dados, você deve utilizar o comando `example_notebook` através do `GNU Make`. Esse comando, fará a configuração do Container para que você possa executar o Jupyter Notebook através de uma interface [Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/):

``` sh
make example_notebook

#> (omitted)    | [C 2022-05-02 02:09:19.813 ServerApp]
#> (omitted)    |
#> (omitted)    |     To access the server, open this file in a browser:
#> (omitted)    |         file:///home/jovyan/.local/share/jupyter/runtime/jpserver-7-open.html
#> (omitted)    |     Or copy and paste one of these URLs:
#> (omitted)    |         http://7bed3d1c3851:8888/lab?token=e6ad88f2a1b6358e1de88ea5a99ba3fd0b872293d3c9e845
#> (omitted)    |      or http://127.0.0.1:8888/lab?token=e6ad88f2a1b6358e1de88ea5a99ba3fd0b872293d3c9e845
```

Ao executar este comando, será exibido em seu terminal o endereço para acesso ao Jupyter Lab através de uma interface web. Utilize seu navegador e acesse esse endereço:

``` sh
firefox http://127.0.0.1:8888/lab?token=e6ad88f2a1b6358e1de88ea5a99ba3fd0b872293d3c9e845
```

Após acessar, seguindo a organização deste RC, acesse o arquivo de processamento que está na seguinte estrutura de diretórios: `analysis > notebook > research-processing.ipynb`.

Para exemplificar todo esse processo, abaixo, tem-se um vídeo que apresenta cada um dos passos mencionados:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/harmonization-jupyter.gif){ width="1024" }
  <figcaption>Configuração do Jupyter Notebook para o processamento dos dados</figcaption>
</figure>

Após a execução, os produtos gerados estarão disponíveis no diretório `analysis/data/derived_data`

!!! tip "Removendo dados"

    Após os testes, caso você deseje remover os dados de entrada/saída, de modo que eles não ocupem espaço em seu disco, utilize através do `GNU Make` o comando `example_cleanup_data`:

    ``` sh
    make example_cleanup_data
    ```

    Note que isso apagará todos os dados. Fazendo isso, para a próxima execução, o *download* dos dados deverá ser realizado novamente.

## Processando dados com Dagster

A segunda abordagem para o processamento dos dados baixados é feita com o uso do Dagster. Com essa ferramenta faz-se a execução do fluxo de processamento dos dados em formato *batch*.

!!! tip "Mais Dagster"

    Para saber mais sobre os Dagster neste RC, consulte a Seção [Scripts de processamento - Dagster](/pt/tools/processing/#dagster).

Para fazer o uso do Dagster e processar os dados, você deve utilizar o comando `example_pipeline` através do `GNU Make`. Esse comando fará a configuração do Container para que você possa acessar o Dagster através da interface [DagIt](https://docs.dagster.io/0.12.15/concepts/dagit/dagit):

``` sh
make example_pipeline

#> (omitted)
#> (omitted)    |   Welcome to Dagster!
#> (omitted)    |
#> (omitted)    |   If you have any questions or would like to engage with the Dagster team, please join us on Slack
#> (omitted)    |   (https://bit.ly/39dvSsF).
#> (omitted)    |
#> (omitted)    | Serving on http://0.0.0.0:3000 in process 1
```

Ao executar este comando, será exibido em seu terminal o endereço para acessar o DagIt. Utilize seu navegador e acesse esse endereço:

``` sh
firefox http://127.0.0.1:3000
```

!!! note "Pro tip"

    O endereço apresentado no terminal é `0.0.0.0` e o acesso é feito pelo endereço `127.0.0.1` no exemplo acima. Isso é possível já que, `0.0.0.0` significa que qualquer endereço pode acessar o serviço criado.


Ao acessar o endereço, você estará no DagIt e poderá começar a processar os dados. A Figura abaixo apresenta um exemplo da interface DagIt que você verá:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-01.svg){ width="1024" }
  <figcaption>Exemplo de interface DagIt.</figcaption>
</figure>

Para começar a processar os dados, na interface DagIt, selecione a opção `Playground`:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-02.svg){ width="1024" }
  <figcaption>Opção Playground na interface DagIt.</figcaption>
</figure>

Ao acessar a aba `Playground`, você verá um campo para a definição das configurações que devem ser consideradas no processamento. Essa configuração é utilizada para determina quais serão os dados de entrada, dados auxiliares e também o local onde os produtos gerados devem ser salvos. As opções dessa configuração deverão ser definidas para que os dados baixados sejam considerados.

A figura abaixo apresenta o campo onde a configuração deve ser determinada.

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-03.svg){ width="1024" }
  <figcaption>Campo de configuração DagIt.</figcaption>
</figure>

Para te auxiliar nessa configuração, no momento em que os dados foram baixados (Subseção [Download dos dados](/pt/reproducible-research/minimal-example/#download-dos-dados)), o *script* [Example toolkit](/pt/tools/utilitary/#example-toolkit) também fez a geração da configuração Dagster necessária para utilizar os dados. Esse arquivo de configuração está disponível no diretório `analysis/pipeline/`, com o nome `config.yaml`.

!!! note "Configuração Dagster e Example toolkit"

    Para saber mais sobre o formato de configuração Dagster e como ele pode ser adaptado para seu contexto, por favor, consulte a Seção de referência [Dagster - Configurações](/pt/tools/processing/#configuracoes_1).

    Adicionalmente, caso você deseje entender o funcionamento do [Example toolkit](/pt/tools/utilitary/#example-toolkit), consulte a Seção de referência [Scripts auxiliares](/pt/tools/utilitary/#scripts-auxiliares).

Copie o conteúdo do arquivo `config.yaml` e cole no campo de configuração na interface DagIt:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-04.svg){ width="1024" }
  <figcaption>Campo de configuração DagIt (Preenchido).</figcaption>
</figure>

Feito isso, inicie o processamento clicando em `Launch Execution`.

Para exemplificar cada um desses passos, abaixo, tem-se um vídeo com cada uma das etapas de configuração e uso Dagster mencionadas anteriormente:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/harmonization-dagster.gif){ width="1024" }
  <figcaption>Configuração do Dagster para o processamento dos dados</figcaption>
</figure>

Após a execução, os produtos gerados estarão disponíveis no diretório `analysis/data/derived_data`.

!!! tip "Removendo dados"

    Após os testes, caso você deseje remover os dados de entrada/saída, de modo que eles não ocupem espaço em seu disco, utilize através do `GNU Make` o comando `example_cleanup_data`:

    ``` sh
    make example_cleanup_data
    ```

    Note que isso apagará todos os dados. Fazendo isso, para a próxima execução, o *download* dos dados deverá ser realizado novamente.
