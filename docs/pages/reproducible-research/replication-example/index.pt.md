*[RC]: Research Compendium

# Exemplo de replicação

!!! attention "Pré-requisitos"

    Antes de iniciar esse exemplo, certifique-se de ter os [pré-requisitos](/pt/reproducible-research/#pre-requisitos) instalados em seu ambiente de trabalho.

!!! attention "Exemplo base"

    Esse é um exemplo que utiliza os materiais deste RC para o processamento de dados de uma região que não foi considerada no artigo original. O objetivo é mostrar que a ferramenta tem características que as tornam reprodutíveis e replicáveis.

    Sendo assim, caso você não tenha feito o primeiro exemplo ([Exemplo mínimo](/pt/reproducible-research/minimal-example/)), recomenda-se que antes de começar esse, você realize o anterior.


## Download do Research Compendium

O primeiro passo para a realização desse exemplo, é o *download* deste RC e todos os seus materiais. Para isso, em um terminal, utilize a ferramenta `git` e faça o [clone](https://git-scm.com/docs/git-clone) do repositório onde o RC está armazenado:

``` sh
git clone https://github.com/brazil-data-cube/Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance
```

Após o [clone](https://git-scm.com/docs/git-clone), um novo diretório será criado no diretório em que você está. O nome deste novo diretório é `Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance`:

``` sh
ls -ls .

#> 4 drwxrwxr-x 3 ubuntu ubuntu 4096 May  2 00:44 Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance
```

Agora, acesse o diretório `Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance` e liste os conteúdos:

*Mudando de diretório*
``` sh
cd Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance
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

Como você pode observar, o conteúdo do diretório representa todos os materiais deste RC. Esse será o conteúdo base utilizado para a realização desse tutorial.

## Download dos dados

Para realizar o *download* dos dados necessários para esse exemplo de replicação, pode-se utilizar o seguinte comando:

``` sh
make replication_ download_data
```

Verifique se os dados foram baixados no diretório `analysis/data/examples/replication_example/`. Caso tudo esteja correto, o conteúdo desse diretório deverá ser parecido com o apresentado abaixo:

```
.
├── landsat8_data
├── lasrc_auxiliary_data
├── scene_id_list
└── sentinel2_data
```

## Processamento de dados

Para realizar o processamento dos dados, como já mencionado nas Seções anteriores, tem-se disponível duas opções: `Jupyter Notebook` ou `Dagster`.

Para ambas abordagens adotadas, tem-se comandos de automação no `Makefile`. Sendo assim, nos tópicos abaixo, de forma resumida, são apresentadas as formas com que cada um desses ambientes podem ser carregados com comandos simples:

*Jupyter Notebook*

``` sh
make replication_notebook
```

*Dagster*

``` sh
make replication_pipeline
```

Com o ambiente escolhido, o processamento e análise dos dados pode ser realizado.
