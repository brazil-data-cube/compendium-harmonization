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

### Evaluating Landsat-8 and Sentinel-2 Nadir BRDF Adjusted Reflectance (NBAR) on South of Brazil through a Reproducible and Replicable Workflow

[![rc](https://img.shields.io/badge/research%20compendium-ready-brightgreen)](#)

Essa é a documentação oficial do `Research Compendium` (RC), com todos os materiais (Códigos, dados, e ambientes computacionais) necessários para a reprodução, replicação e avaliação dos resultados apresentados no artigo:

!!! quote ""

    Marujo *et al* (2022). `Evaluating Landsat-8 and Sentinel-2 Nadir BRDF Adjusted Reflectance (NBAR) on South of Brazil through a Reproducible and Replicable Workflow`. Paper será submetido em Junho de 2022.

#### Organização do Research Compendium

A organização definida para este RC, visa facilitar a utilização dos códigos implementados para a geração dos resultados apresentados no artigo. Para isso, os códigos de processamento são disponibilizados em uma estrutura de [exemplos](/pt/reproducible-research/) que permitem a execução sem dificuldades, fazendo com que outros possam reproduzir e replicar o estudo realizado.

Esses códigos, são armazenados no diretório `analysis`, o qual possui três subdiretórios:

- [:file_folder: analysis/notebook](analysis/notebook): Diretório com a versão Jupyter Notebook do fluxo de processamento implementado no artigo associado a este RC. Para mais informações, consulte a Seção de referência [Scripts de processamento](/pt/tools/processing/);

- [:file_folder: analysis/pipeline](analysis/pipeline): Diretório com a versão Dagster do fluxo de processamento implementado no artigo associado a este RC. Para mais informações, consulte a Seção de referência [Scripts de processamento](/pt/tools/processing/);

- [:file_folder: analysis/data](analysis/data/): Diretório para armazenar os dados de entrada e saída gerados. Contém os seguintes subdiretórios:

    - [:file_folder: examples](analysis/data/examples): Diretório com os dados (Entrada/Saída) dos exemplos disponibilizados neste RC. Ao todo, são dois exemplos. Para mais informações sobre os exemplos, consulte o Capítulo [Processamento de dados](/pt/reproducible-research/);

    - [:file_folder: original_scene_ids](analysis/data/original_scene_ids): Diretório para armazenar os arquivos de índices de cenas originais utilizados na produção dos resultados dos artigos. Esses dados podem ser aplicados nos códigos disponibilizados nos diretórios [analysis/notebook](analysis/notebook) e [analysis/pipeline](analysis/pipeline) para a reprodução do resultados do artigo.

Por padrão, os dados de entrada, por conta do tamanho dos arquivos, não são armazenados diretamente no diretório de dados (`analysis/data/`). Ao contrário disso, como é descrito em detalhes na Seção de referência [Scripts auxiliares](/pt/tools/utilitary/), eles são disponibilizados no GitHub Release Assets do repositório do RC.

Para a construção dos [scripts de processamento](/pt/tools/processing/) disponíveis no diretório `analysis`, fez-se a criação de diversas [bibliotecas de *software*](/pt/tools/libraries/) e [*scripts* auxiliares](/pt/tools/utilitary/). O código fonte de parte dessas ferramentas fica disponível no diretório `tools` deste RC. Nesse diretório, tem-se quatro subdiretórios, sendo eles:

- [:file_folder: tools/auxiliary-library](tools/auxiliary-library): Código fonte da biblioteca [research-processing](/pt/tools/libraries/#research-processing-python-library-research-processing), a qual fornece as operações de alto nível para o processamento de dados deste RC;

- [:file_folder: tools/calculate-checksum](tools/calculate-checksum): Código fonte do *script* [calculate-checksum](/pt/tools/utilitary/#calculate-checksum-e-github-asset-upload), criado para calcular o *checksum* dos arquivos deste RC antes do compartilhamento;

- [:file_folder: tools/example-toolkit](tools/example-toolkit): Código fonte do *script* [example-toolkit](/pt/tools/utilitary/#example-toolkit), criado para facilitar o *download* e validação dos dados de exemplo do GitHub Release Assets;

- [:file_folder: tools/github-asset-upload](tools/github-asset-upload): Código fonte do *script* [github-asset-upload](/pt/tools/utilitary/#calculate-checksum-e-github-asset-upload), criado para facilitar o *upload* dos dados de exemplo para o GitHub Release Assets.

Outro diretório disponível neste RC é o `composes`. Nesse diretório, estão arquivos de configuração do [Docker Compose](https://docs.docker.com/compose/) dos ambientes computacionais necessários para a execução dos exemplos disponíveis neste RC. Para mais informações sobre os ambientes computacionais do RC, consulte a Seção de referência [Ambientes computacionais](/pt/tools/environment/).

No diretório `composes`, tem-se dois subdiretórios:

- [:file_folder: composes/minimal](composes/minimal): Diretório com os Docker Composes para a execução do [Exemplo mínimo](/pt/reproducible-research/minimal-example/) fornecido neste RC;

- [:file_folder: composes/replication](composes/replication): Diretório com os Docker Composes para a execução do [Exemplo de replicação](/pt/reproducible-research/replication-example/) fornecido neste RC.

Para mais informações sobre os exemplos, consulte a Seção [Processamento de dados](/pt/reproducible-research/).

De forma complementar ao diretório `composes`, tem-se o diretório `docker`. Nesse diretório, estão armazenados os arquivos [Dockerfile](https://docs.docker.com/engine/reference/builder/) utilizados para a construção dos ambientes utilizados nos Docker Composes. Esse diretório possui dois subdiretórios:

- [:file_folder: docker/notebook](docker/notebook): Diretório com os [Dockerfile](https://docs.docker.com/engine/reference/builder/) do ambiente necessário para a [execução da versão Jupyter Notebook](/pt/tools/environment/#jupyter-notebook) do fluxo de processamento deste RC.

- [:file_folder: docker/pipeline](docker/pipeline): Diretório com os [Dockerfile](https://docs.docker.com/engine/reference/builder/) do ambiente necessário para a [execução da versão Dagster](/pt/tools/environment/#dagster) do fluxo de processamento deste RC.

Além desses diretórios, há também alguns arquivos fundamentais para o uso dos materiais deste RC, são eles:

- [Vagrantfile](Vagrantfile) e `bootstrap.sh`: Arquivos [Vagrant](https://www.vagrantup.com/) utilizados para a construção de uma máquina virtual com o ambiente completo para a execução dos [Scripts de processamento](/pt/tools/processing/) disponíveis no diretório `analysis`. Para mais informações, consulte a Seção de referência [Ambientes computacionais - Máquina virtual com Vagrant](/pt/tools/environment/#maquina-virtual-com-vagrant);

- [Makefile](Makefile): Arquivo de definição `GNU Make` que facilita a utilização dos materiais disponíveis nos diretórios `analysis` e `composes`. O arquivo `setenv.sh` é utilizado pelo `Makefile` para a definição do usuário que fará a execução do Jupyter Notebook. Mais informações são fornecidos na Seção [Processamento de dados](/pt/reproducible-research/).
