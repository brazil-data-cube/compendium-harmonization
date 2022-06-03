*[RC]: Research Compendium
*[CLI]: Command-Line Interface

# Ambientes computacionais

Por trás de cada etapa empregada nos [scripts de processamento](/pt/tools/processing/), conforme apresentado nas Seções anteriores, existem diversas ferramentas e bibliotecas de *software* sendo utilizadas.

Algumas dessas ferramentas fazem o uso de tecnologias especiais para a execução de suas operações, como é o caso da [biblioteca research-processing](/pt/tools/libraries/#research-processing-python-library-research-processing), que utiliza Docker Containers para executar as funções de processamento em ambientes isolados. Outras ferramentas, apenas fazem o uso do ambiente subjacente para sua execução, como é o caso do *script* auxiliar [Example toolkit](/pt/tools/utilitary/#example-toolkit). Neste caso, é exigido que o ambiente subjacente esteja configurado e pronto para executar o *script*.

Em ambos os cenários apresentados, há desafios específicos no que diz respeito ao gerenciamento dos ambientes computacionais utilizados. Por exemplo, pode ser necessário configurações específicas no *software* para que ele opere junto a [biblioteca research-processing](/pt/tools/libraries/#research-processing-python-library-research-processing), enquanto que configurações específicas podem ser exigidas no uso do [Example toolkit](/pt/tools/utilitary/#example-toolkit).

Para resolver esses problemas e evitar que a configuração dos ambientes computacionais utilizados, suas dependências e necessidades específicas causem problemas para a reprodutibilidade e replicabilidade dos [scripts de processamento](/pt/tools/processing/) criados neste RC, todos os ambientes necessários para a execução das ferramentas foram organizadas em Docker Images. Essas, representam "pacotes de ambientes" prontos para uso, onde tem-se todas as dependências e configurações necessárias para a execução de uma ferramenta específica.

Nesta Seção, é feita a apresentação de cada uma dessas Docker Images, suas características, configurações e formas de uso. Deve-se notar que, essas Docker Images não foram criadas para um sistema operacional específico, podendo ser utilizado em qualquer sistema que tenha suporte ao Docker. No entanto, deve-se notar que nesta documentação, os comandos e formas de configuração apresentados, consideram como base o uso do Sistema Operacional Linux Ubuntu 20.04. Desta forma, mudanças podem ser necessárias nos comandos caso você esteja utilizando um sistema operacional diferente, como é o caso do Windows.


!!! note "Mudanças entre os sistemas operacionais"


    Embora tenhamos esperança de que os comandos e dicas apresentados neste documento possam ser utilizados sem problemas em sistemas operacionais Linux (e.g., Ubuntu, Debian) e MacOS, não há uma garantia de que isso sempre se manterá verdadeiro. Além disso, para aqueles que utilizam Windows, mudanças nos comandos podem ser necessárias.

    Com o objetivo de evitar que os materiais produzidos não possam ser utilizados por essa barreira tecnológica, nós criamos uma Máquina Virtual Ubuntu 20.04, com todas as dependências necessárias (e.g., [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/)) para que os comandos apresentados aqui, possam ser utilizados.

    Caso você precise utilizar essa Máquina Virtual, por favor, consulte a Seção [Máquina Virtual com Vagrant](/pt/tools/environment/#maquina-virtual-com-vagrant).


## Docker Images <img src="/assets/tools/environment/docker/docker-logo.png" align="right" width="160"/>

Neste RC, existem diferentes tipos de ambientes que estão sendo configurados dentro das Docker Images. No geral, essas Docker Images podem ser classificadas em dois tipos:

**Executable**

Ferramentas de linha de comando (CLI, do inglês *Command-Line Interface*) são simples e diretas de utilizar e permitem que automações sejam realizadas durante as etapas de processamento. Seguindo esse pensamento, as Docker Images `Executable` são aquelas criadas para armazenar um *script* que pode ser executado como uma CLI. Para isso, esse tipo de Docker Image tem as seguintes propriedades:

1. Cada execução da Docker Image representa uma execução individual da ferramenta a qual está associada;
2. Parâmetros podem ser passados durante a execução da Docker Image. Esses parâmetros são utilizados para configurar a ferramenta que é executada;
3. Docker Volumes e variáveis de ambientes, também podem ser utilizados para configurar a Docker Image, sendo utilizados, por exemplo, para determinar as entradas e saídas e configurações da ferramenta executada.

**Environment**

Diferente das Docker Images `Executable`, essas Docker Images são criadas para servir como um ambiente completo que será utilizado para a execução de uma ferramenta, como um Jupyter Notebook ou Dagster Web Interface.

A principal diferença entre esses dois tipos de Docker Images criados neste RC está em sua finalidade. Enquanto as `Executables` representam as ferramentas executáveis, as `Environment` representam ambientes de fato, para uso e execução de ferramentas específicas.

Nas Subseções a seguir, as Docker Images criadas neste RC serão apresentadas.

### Sen2Cor 2.9.0
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/sen2cor)

[Sen2cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/) é um processador de correção atmosférica para produtos Sentinel-2. Ele recebe como entrada produtos Sentinel-2 em nível de radiância de topo de atmosféra (ToA), também chamados Level-1C (L1C) e gera produtos "Bottom of the atmosphere (BOA) reflectance", além de fornecer também uma classificação da cena. Com o uso dessa classificação, é possível, por exemplo, identificar *pixels* com influência de nuvem, sombra de nuvem ou neve.

!!! note "Mais sobre o Sen2Cor"

    Para mais informações sobre o Sen2Cor, consulte o [Manual oficial do usuário](http://step.esa.int/thirdparties/sen2cor/2.9.0/docs/S2-PDGS-MPC-L2A-SRN-V2.9.0.pdf).


De modo a possibilitar que as execuções realizadas com Sen2Cor fossem reprodutíveis e reutilizáveis, preparou-se uma Docker Image específica para essa ferramenta. Essa Docker Image, nomeada de `sen2cor`, possui todas as dependências e configurações necessárias para a execução do Sen2Cor.

!!! note "Versões do Sen2Cor"

    O [Sen2Cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/), é um *software* mantido e distribuído pela [**E**uropean **S**pace **A**gency](https://www.esa.int/) (ESA) e continua lançando novas versões. Neste RC, foi considerado paras as atividades com o Sen2Cor, a versão `2.9.0`.

Os tópicos a seguir, apresentam as principais características desta Docker Image, como volumes, dados auxiliares necessários e forma de utilização.

**Dados auxiliares**

Para a execução da `sen2cor`, é necessário o uso de alguns dados auxiliares. Esses dados, dizem respeito ao [ESACCI-LC for Sen2Cor data package](http://maps.elie.ucl.ac.be/CCI/viewer/download.php), que é utilizado pelos módulos de identificação de nuvens e classificação. A obtenção dos dados pode ser feita seguindo os passos listados abaixo:

1. Acesse o endereço: [http://maps.elie.ucl.ac.be/CCI/viewer/download.php](http://maps.elie.ucl.ac.be/CCI/viewer/download.php);
2. Faça seu cadastro (caso não tenha) e login;
3. Após o login, procure pelo pacote `ESACCI-LC for Sen2Cor data package`;
4. Faça o *download* desse pacote (Arquivo `zip`);
5. Extraia o conteúdo em um diretório. Recomenda-se para esse diretório o nome `CCI4SEN2COR`.

Após a extração dos arquivos, o diretório de destino deverá conter os seguintes arquivos:

- `ESACCI-LC-L4-WB-Map-150m-P13Y-2000-v4.0.tif` (GeoTIFF);
- `ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7.tif` (GeoTIFF);
- `ESACCI-LC-L4-Snow-Cond-500m-P13Y7D-2000-2012-v2.0` (Directório).

**Volumes**

Para a utilização da `sen2cor`, é necessário a definição de alguns Docker Volumes. Esses volumes, especificam os dados de entrada, saída, arquivos de configuração e dados auxiliares utilizados pela ferramenta. Abaixo, esses volumes são listados e descritos:


`Dados de entrada` (Obrigatório)

:   Diretório com os dados de entrada. Esse volume, deve mapear um diretório da máquina local para o diretório `/mnt/input_dir` do Container. Recomenda-se que esse volume seja somente leitura, para garantir que nenhuma modificação será feita nos dados de entrada.


`Dados de saída` (Obrigatório)

:   Diretório onde os produtos gerados serão armazenados. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/output_dir` do Container.


`Dados auxiliares` (Obrigatório)

:   Diretório com os dados auxiliares necessário para o funcionamento do Sen2Cor. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/sen2cor-aux/CCI4SEN2COR` do Container.

`Arquivo de configuração` (Opcional)

:   Volume para a definição do arquivo de configuração `L2A_GIPP.xml`. O volume criado, deve mapear o arquivo `L2A_GIPP.xml` da máquina local para o arquivo `/opt/sen2cor/2.9.0/cfg/L2A_GIPP.xml` no Container.

`Dados SRTM` (Opcional)

:   Volume para a especificação do diretório com imagens SRTM que devem ser utilizados nas etapas do Sen2Cor. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/sen2cor-aux/srtm` do Container.

**Exemplo de utilização (Docker CLI)**

O código abaixo, apresenta um exemplo de utilização da Docker Image `sen2cor` através da Docker CLI.

!!! tip "Nome da imagem"

    No comando apresentado abaixo, a Docker Image `sen2cor` é identificada como `marujore/sen2cor:2.9.0` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `2.9.0`.

!!! warning "Formatação do comando"

    O comando abaixo é criado para ser ditádico. Caso você queira utiliza-lo, não esqueça de substituir os valores e remover os espaços entre cada linha.

``` sh
docker run --rm \

    # Volume: Dados de entrada
    --volume /path/to/input_dir:/mnt/input_dir:ro \

    # Volume: Dados de saída
    --volume /path/to/output_dir:/mnt/output_dir:rw \

    # Dados auxiliares: Diretório CCI4SEN2COR
    --volume /path/to/CCI4SEN2COR:/mnt/aux_data \

    # Arquivo de configuração: L2A_GIPP.xml (Opcional)
    --volume /path/to/L2A_GIPP.xml:/opt/sen2cor/2.9.0/cfg/L2A_GIPP.xml \

    # Dados SRTM (Opcional)
    --volume /path/to/srtm:/root/sen2cor/2.9/dem/srtm \

    # Especificação da Docker Image e cena a ser processada
    marujore/sen2cor:2.9.0 S2A_MSIL1C_20210903T140021_N0301_R067_T21KVR_20210903T172609.SAFE
```

A execução do comando apresentado acima, fará a criação de um Docker Container `sen2cor`. Esse Docker Container fará o processamento da cena `S2A_MSIL1C_20210903T140021_N0301_R067_T21KVR_20210903T172609.SAFE`. Neste comando, deve-se notar que, o diretório de entrada (`/path/to/input_dir`) especificado, deve conter um subdiretório com o mesmo nome da cena escolhida, neste caso `S2A_MSIL1C_20210903T140021_N0301_R067_T21KVR_20210903T172609.SAFE`. Além disso, é esperado que nesse subdiretório, todos os dados da cena estejam disponíveis para o processamento.

Para mais informações, consulte o [repositório do GitHub](https://github.com/marujore/sen2cor-docker), onde tem-se mantido o versionamento das mudanças realizadas na Docker Image `sen2cor`.

### LaSRC 2.0.1
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/lasrc)

[LaSRC](https://ntrs.nasa.gov/api/citations/20190001670/downloads/20190001670.pdf) é um processador de correção atmosférica originalmente proposto para produtos Landsat-8 Collection 1, sendo posteriormente adaptado para ser capaz também de corrigir produtos Sentinel-2. Ele recebe como entrada produtos Landsat em Número Digital (DN, do inglês *Digital Number*) ou produtos Sentinel-2 em nível de radiância de topo de atmosféra (ToA), também chamados Level-1C (L1C). O resultado desse processador consiste em produtos em nível reflectância de superfície (SR, do inglês *Surface Reflectance*).

Para facilitar a utilização do LaSRC neste RC, e garantir que a execução seja reprodutível e reutilizável, fez-se a criação de um Docker Image para o LaSRC, nomeada de `lasrc`. A `lasrc`, possui todas as dependências e configurações necessárias para a execução do processador LaSRC.

Os tópicos a seguir, apresentam as principais características desta Docker Image, como volumes, dados auxiliares necessários e forma de utilização.

**Dados auxiliares**

Para a execução da `lasrc`, é necessário a definição de alguns dados auxiliares. Para obter esses dados, você pode seguir os passos listados abaixo:

1. Acesse: [https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/](https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/);
2. Faça o download de todos os conteúdos disponíveis listados, com exceção do diretório `LADS`.

Os dados do diretório `LADS` também são requeridos para a utilização do LaSRC, no entanto, esse diretório contém dados diários de 2013 até os dias atuais, o que representa um grande volume de dados. Para tornar o processo mais rápido, recomenda-se que seja feito o *download* apenas dos arquivos `LADS` das datas que serão processadas.

!!! tip "Seleção de arquivos LADS"

    Cada arquivo LADS refere-se a uma data do ano. Sendo assim, para processar uma imagem do dia 1° de Janeiro de 2017, deve-se obter o arquivo LADS `L8ANC2017001.hdf_fused` em que 2017 representa o ano e o valor `001` a data 1° de Janeiro em formato Juliano.

Ao final da aquisição dos dados auxiliares, o diretório onde os dados foram armazenados deve ter a seguinte estrutura:

```
.
├── CMGDEM.hdf
├── LADS
├── LDCMLUT
├── MSILUT
└── ratiomapndwiexp.hdf
```

**Volumes**

Para a utilização da `lasrc`, é necessário a definição de alguns Docker Volumes. Esses volumes, especificam os dados de entrada, saída e dados auxiliares utilizados pela ferramenta durante o processamento. Abaixo, tem-se um descritivo de todos volumes que devem ser criados durante a execução da Docker Image LaSRC:

`Dados de entrada` (Obrigatório)

:   Diretório com os dados de entrada. Esse volume, deve mapear um diretório da máquina local para o diretório `/mnt/input_dir` do Container. Recomenda-se que esse volume seja somente leitura, para garantir que nenhuma modificação será feita nos dados de entrada.


`Dados de saída` (Obrigatório)

:   Diretório onde os produtos gerados serão armazenados. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/output_dir` do Container.


`Dados auxiliares` (Obrigatório)

:   Diretório com os dados auxiliares necessário para o funcionamento do LaSRC. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/atmcor_aux/lasrc/L8` do Container.

**Exemplo de utilização (Docker CLI)**

Os códigos abaixo apresentam dois exemplos de utilização do `lasrc`, através da Docker CLI. No primeiro exemplo, faz-se o processamento de uma cena Landsat-8/OLI, enquanto no segundo é processado uma cena Sentinel-2/MSI.

!!! tip "Nome da imagem"

    Nos comandos apresentados abaixo, a Docker Image `lasrc` é identificada como `marujore/lasrc:2.0.1` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `2.0.1`.

!!! warning "Formatação do comando"

    O comando abaixo é criado para ser ditádico. Caso você queira utiliza-lo, não esqueça de substituir os valores e remover os espaços entre cada linha.

*Exemplo para dados Landsat-8/OLI*

``` sh
docker run --rm \

    # Volume: Dados de entrada
    --volume /path/to/input/:/mnt/input-dir:rw \

    # Volume: Dados de saída
    --volume /path/to/output:/mnt/output-dir:rw \

    # Dados auxiliares (Dados L8/LADS)
    --volume /path/to/lasrc_auxiliaries/L8:/mnt/atmcor_aux/lasrc/L8:ro \

    # Especificação da Docker Image e cena a ser processada
    --tty marujore/lasrc:2.0.1 LC08_L1TP_220069_20190112_20190131_01_T1
```

*Exemplo para dados Sentinel-2/MSI*

``` sh
 docker run --rm \

    # Volume: Dados de entrada
    --volume /path/to/input/:/mnt/input-dir:rw \

    # Volume: Dados de saída
    --volume /path/to/output:/mnt/output-dir:rw \

    # Dados auxiliares (Dados L8/LADS)
    --volume /path/to/lasrc_auxiliaries/L8:/mnt/atmcor_aux/lasrc/L8:ro \

    # Especificação da Docker Image e cena a ser processada
    --tty marujore/lasrc:2.0.1 S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE
```

Como pode-se notar, a diferença para o uso da `lasrc` para os dados dos diferentes satélite-sensor, está apenas na especificação do nome da cena. Deve-se notar também que, é esperado, para ambos os casos que, no diretório de entrada (`/path/to/input/`) tenha subdiretórios com as cenas específicas, neste caso `LC08_L1TP_220069_20190112_20190131_01_T1` e `S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE`. Além disso, é esperado que nesses subdiretórios, todos os dados das cenas estejam disponíveis para o processamento.

Para mais informações, consulte o [repositório do GitHub](https://github.com/marujore/lasrc-docker), onde tem-se mantido o versionamento das mudanças realizadas na Docker Image `lasrc`.

### L8Angs
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/l8angs)

[Landsat Ang Tool](https://www.usgs.gov/landsat-missions/landsat-tools) é uma ferramenta desenvolvida e mantida pela [**U**nited **S**tates **G**eological **S**urvey](https://www.usgs.gov/). A ferramenta é capaz de utilizar arquivos `ANG.txt` fornecidos junto à produtos Landsat-8 para gerar bandas de angulos por *pixel*, no caso os ângulos solar azimutal (`SAA`), solar zenital (`SZA`), sensor azimutal (`VAA`) e sensor zenital (`VZA`). As bandas são geradas com a mesma resolução espacial das bandas espectrais do sensor OLI acoplados ao satélite Landsat-8.

!!! note "Mais sobre o Landsat Ang Tool"

    Para informações detalhadas sobre o Landsat Ang Tool, consulte o [site oficial da USGS sobre a ferramenta](https://www.usgs.gov/core-science-systems/nli/landsat/solar-illumination-and-sensor-viewing-angle-coefficient-files?qt-science_support_page_related_con=1#qt-science_support_page_related_con).

Neste RC, as imagens Landsat-8/OLI (Collection-2) são obtidas já processadas em nível de reflectância de superfície (L2). Entretanto, para processamentos posteriores, é necessário a geração das bandas de ângulos. Neste caso, faz-se o uso do [Landsat Ang Tool](https://www.usgs.gov/landsat-missions/landsat-tools).

A instalação e configuração do [Landsat Ang Tool](https://www.usgs.gov/landsat-missions/landsat-tools) pode tornar difícil a reprodução e replicação no futuro. Sendo assim, para facilitar as operações deste RC que utilizam essa ferramenta, fez-se a criação de uma Docker Image específica para ela, nomeada de `l8angs`.

Os tópicos a seguir, apresentam as principais características desta Docker Image, como volumes e dados auxiliares necessários para a execução. Também são apresentados exemplos de utilização através da Docker CLI.

**Volumes**

Para a utilização da `l8angs`, é necessário a definição do seguinte volume, durante a execução:

`Dados de entrada` (Obrigatório)

:   Diretório com os dados de entrada. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/input-dir` do Container. Os dados gerados são criados no mesmo diretório de entrada, sendo este o comportamento padrão da ferramenta.

**Exemplo de utilização (Docker CLI)**

O código abaixo, apresenta um exemplo de utilização da Docker Image `l8angs` através da Docker CLI.

!!! tip "Nome da imagem"

    Nos comandos apresentados abaixo, a Docker Image `l8angs` é identificada como `marujore/l8angs:2.0.1` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

!!! warning "Formatação do comando"

    O comando abaixo é criado para ser ditádico. Caso você queira utiliza-lo, não esqueça de substituir os valores e remover os espaços entre cada linha.

``` sh
docker run --rm \

    # Volume: Dados de entrada
    -v /path/to/input/:/mnt/input-dir:rw \

    # Especificação da Docker Image e cena a ser processada
    marujore/l8angs:latest LC08_L2SP_222081_20190502_20200829_02_T1
```

A execução do comando apresentado acima, fará a criação de um Docker Container `l8angs`. Esse Docker Container fará o processamento da cena `LC08_L2SP_222081_20190502_20200829_02_T1`. Neste comando, deve-se notar que, o diretório de entrada (`/path/to/input/`) especificado, deve conter um subdiretório com o mesmo nome da cena escolhida, neste caso `LC08_L2SP_222081_20190502_20200829_02_T1`. Além disso, é esperado que nesse subdiretório, todos os dados da cena estejam disponíveis para o processamento.

Para mais informações, consulte o [repositório do GitHub](https://github.com/marujore/landsat-angles-docker)), onde tem-se mantido o versionamento das mudanças realizadas na Docker Image `l8angs`.

### Sensor Harm
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/nbar)

Neste RC, as imagens Landsat-8 Collection-2 já obtidas em nível de reflectância de superfície (L2) e as imagens Sentinel-2 (processadas para reflectância de superfície tanto utilizando Sen2cor quanto LaSRC) são harmonizadas utilizando a biblioteca [sensor-harm](/pt/tools/libraries/#sensor-harmonization-python-library-sensor-harm). Para potencializar a reprodução e replicação no uso dessa ferramenta, fez-se a criação da Docker Image `nbar`. Nesta Image, estão disponíveis todas as dependências e configurações necessárias para a execução do [sensor-harm](/pt/tools/libraries/#sensor-harmonization-python-library-sensor-harm).

Os tópicos a seguir, apresentam as principais características desta Docker Image, volumes requeridos e exemplos de utilização.

**Volumes**

Para a utilização da `nbar`, é necessário a definição de alguns Docker Volumes. Esses volumes, especificam os dados de entrada e dados auxiliares utilizados pelo sensor-harm. Abaixo, esses volumes são listados e descritos:

`Dados de entrada` (Obrigatório)

:   Diretório com os dados de entrada. Esse volume, deve mapear um diretório da máquina local para o diretório `/mnt/input-dir` do Container. Recomenda-se que esse volume seja somente leitura, para garantir que nenhuma modificação será feita nos dados de entrada.


`Dados de saída` (Obrigatório)

:   Diretório onde os produtos gerados serão armazenados. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/output-dir` do Container.


`Diretório de ângulos` (Obrigatório apenas para dados Landsat-8/OLI)

:   Diretório com os dados de ângulos da cena que será processada. O volume criado, deve mapear um diretório da máquina local para o diretório `/mnt/angles-dir` do Container. Recomenda-se que esse volume seja somente leitura, para garantir que nenhuma modificação será feita nos dados durante o processamento.


**Exemplo de utilização (Docker CLI)**

Os códigos abaixo apresentam dois exemplos de utilização do `nbar`, através da Docker CLI. No primeiro exemplo, faz-se o processamento de uma cena Landsat-8/OLI, enquanto no segundo é processado uma cena Sentinel-2/MSI.

!!! tip "Nome da imagem"

    Nos comandos apresentados abaixo, a Docker Image `nbar` é identificada como `marujore/nbar:latest` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

!!! warning "Formatação do comando"

    O comando abaixo é criado para ser ditádico. Caso você queira utiliza-lo, não esqueça de substituir os valores e remover os espaços entre cada linha.

*Exemplo para dados Landsat-8/OLI*

``` sh
docker run --rm \

    # Volume: Dados de entrada
    --volume /path/to/input/:/mnt/input-dir:ro \

    # Volume: Dados de saída
    --volume /path/to/output:/mnt/output-dir:rw \

    # Diretório de ângulos (Apenas Landsat-8/OLI)
    --volume /path/to/angles:/mnt/angles-dir:ro \

    # Especificação da Docker Image e cena a ser processada
    --tty marujore/nbar:latest LC08_L1TP_220069_20190112_20190131_01_T1
```

*Exemplo para dados Sentinel-2/MSI*

``` sh
docker run --rm \

    # Volume: Dados de entrada
    --volume /path/to/input/:/mnt/input-dir:ro \

    # Volume: Dados de saída
    --volume /path/to/output:/mnt/output-dir:rw \

    # Diretório de ângulos (Apenas Landsat-8/OLI)
    --volume /path/to/angles:/mnt/angles-dir:ro \

    # Especificação da Docker Image e cena a ser processada
    --tty marujore/nbar:latest S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE
```

Como pode-se notar, a diferença para o uso da `nbar` para os dados dos diferentes satélite-sensor, está apenas na especificação do nome da cena. Deve-se notar também que, é esperado, para ambos os casos que, no diretório de entrada (`/path/to/input/`) tenha subdiretórios com as cenas específicas, neste caso `LC08_L1TP_220069_20190112_20190131_01_T1` e `S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE`. Além disso, é esperado que nesses subdiretórios, todos os dados das cenas estejam disponíveis para o processamento.

Para mais informações, consulte o [repositório do GitHub](https://github.com/marujore/sensor-harm), onde tem-se mantido o versionamento das mudanças realizadas na Docker Image `nbar`.

### Docker Images para Scripts de processamento

Conforme apresentado na Seção [Scripts de processamento](/pt/tools/processing/), foram criados duas formas de realizar a execução da metodologia dos experimentos deste RC. Uma utiliza o [Jupyter Notebook](/pt/tools/processing/#jupyter-notebook), sendo voltada para o processamento interativo dos códigos. A segunda opção, por outro lado, utiliza o [Dagster](/pt/tools/processing/#dagster) e facilita execuções em lote e controle de erro.

Para facilitar a utilização de ambas as abordagens, fez-se a criação de Docker Images com os ambientes necessários à execução de cada um deles. Com isso, evita-se que dependências tenham de ser instaladas ou configuradas para a execução dos [scripts de processamento](/pt/tools/processing/).

Os tópicos a seguir, apresentam as principais características dessas Docker Images, volumes requeridos, configuração e exemplos de utilização.

!!! tip "Funcionamento dos scripts"

    Caso você esteja interessado em reutilizar essas Docker Images, recomenda-se antes a leitura do modo de funcionamento dos [scripts de processamento](/pt/tools/processing/), bem como das [bibliotecas de software](/pt/tools/libraries/) utilizadas por esses *scripts*.

#### Jupyter Notebook
[![docker-image-type](https://img.shields.io/badge/Type-Environment-orange)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/#)

Para a execução da versão Jupyter Notebook, fez-se a criação da Docker Image `research-processing-jupyter`. Essa Docker Image disponibiliza uma interface [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/), com as dependências Python necessárias para a execução dos *scripts*. Além disso, nessa Docker Image, tem-se também o Docker instalado, para que os *scripts* sejam capazes de operar e criar outros Docker Containers de processamento.

!!! note "Base do ambiente"

    A criação da `research-processing-jupyter`, foi realizada utilizando como base a Docker Image [jupyter/minimal-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-minimal-notebook), disponibilizada pelo time de desenvolvimento do projeto [Jupyter](https://jupyter.org/).

    Com isso, todas as [configurações e variáveis de ambientes](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html) disponíveis na Docker Image `jupyter/minimal-notebook` também são aplicáveis a `research-processing-jupyter`.

Nos tópicos abaixo, é feita a apresentação das configurações necessárias para utilizar essa Docker Image. Exemplos de utilização com a CLI do Docker e [Docker Compose](https://docs.docker.com/compose/), também serão apresentados.

**Variáveis de ambiente**

Para a utilização da `research-processing-jupyter`, é necessário definir a seguinte variável de ambiente:

`DATA_DIRECTORY` (Obrigatório)

:   Variável de ambiente para determinar o diretório, na máquina local, onde os dados baixados devem ser salvos.


**Volumes**

A execução do `research-processing-jupyter` deve ser realizada com a definição de dois volumes:

`Volume de dados` (Obrigatório)

:   Volume onde os dados serão armazenados. Seguindo o [modelo de execução](/pt/tools/libraries/#abordagem-de-execucao-das-funcoes) das funções de processamento utilizadas nos *scripts*, esse volume será utilizado por funções dentro do mesmo container (`Local`) ou em outros containers (`Containerized`). Desta forma, a definição desse volume deve ser feita de modo a atender duas exigências:

:     * O volume deve ser do tipo [Bind Mount](https://docs.docker.com/storage/bind-mounts/);
:     * O mapeamento do volume (`Bind Mount`) deve utilizar, na máquina local e no Container, o mesmo caminho definido na variável `DATA_DIRECTORY`.

:   Com essas definições, o volume será visível dentro do Container da `research-processing-jupyter` e também pelos Containers auxiliares de processamentos que forem gerados durante a execução dos [scripts de processamento](/pt/tools/processing/).

`Volume Daemon Socket` (Obrigatório)

:   Para que os scripts sejam capazes de gerar Docker Containers de processamento, é necessário a definição do [Daemon Socket](https://docs.docker.com/engine/reference/commandline/dockerd/#description) como um volume. Ao fazer isso, o Docker dentro do container criado com a imagem `research-processing-jupyter` é capaz de interagir com o Docker da máquina local, permitindo que Containers de processamento sejam criados.

**Definição de usuário**

De forma complementar a definição do `Daemon Socket volume`, para a execução da `research-processing-jupyter`, é necessário especificar um usuário (`UID`) e grupo (`GID`) da máquina local que tenham permissão para interagir com o Docker Daemon. Esses valores, serão aplicados ao usuário padrão do Container, de modo que o Docker permita que ele também interaga com o Docker Daemon da máquina local.

!!! note "Permissões no Docker"

    Caso você esteja interessado em entender os detalhes do motivo por trás da definição dos usuários, recomendamos que você consulte a [documentação oficial do Docker](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

Para que você faça a definição do usuário, no momento da execução da `research-processing-jupyter`, você pode utilizar o parâmetro [--user](https://docs.docker.com/engine/reference/run/#user). Caso você deseje utilizar o Docker Compose, o campo [user](https://docs.docker.com/engine/reference/run/#user) pode ser utilizado para essa definição.

**Exemplo de utilização (Docker CLI)**

Abaixo, faz-se a apresentação de um exemplo de uso da Docker Image `research-processing-jupyter` através da Docker CLI:

!!! tip "Nome da imagem"

    No comando apresentado abaixo, a Docker Image `research-processing-jupyter` é identificada como `marujore/research-processing-jupyter:latest` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

!!! warning "Formatação do comando"

    O comando abaixo é criado para ser ditádico. Caso você queira utiliza-lo, não esqueça de substituir os valores e remover os espaços entre cada linha.

``` sh
docker run \
  --name research-processing-jupyter \

  # Definição do usuário
  --user ${UID}:${GID} \

  # Variáveis de ambiente
  --env JUPYTER_ENABLE_LAB=yes \ # Ativando JupyterLab
  --env DATA_DIRECTORY=/my-data-dir \

  # Volume: Volume de dados
  --volume /my-data-dir:/my-data-dir \

  # Volume: Volume Daemon Socket
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \

  # Porta de rede por onde o serviço poderá ser acessado
  --publish 8888:8888 \

  # Especificação da Docker Image
  marujore/research-processing-jupyter:latest
```

!!! tip "Definição do usuário"

    Para a definição do usuário, utilizando variáveis de ambiente (`${UID}` e `${GID}`), como realizado no comando acima, antes de executar o comando Docker, utilize os seguintes comandos:

    ``` sh
    export UID=`id -u $USER`
    export GID=`cut -d: -f3 < <(getent group docker)`
    ```

Após a execução do comando acima, deverá ser produzir um resultado parecido com o apresentado abaixo:

``` sh
# (Omitted)

[I 2022-04-30 19:22:50.684 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2022-04-30 19:22:50.694 ServerApp]

    To access the server, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/jpserver-7-open.html
    Or copy and paste one of these URLs:
        http://ae88466ccb18:8888/lab?token=0497e15e042d52cfb498a2edf3d2c6e5874e79b4808ca860
     or http://127.0.0.1:8888/lab?token=0497e15e042d52cfb498a2edf3d2c6e5874e79b4808ca860
```

Após a execução deste comando, utilizando um navegador e acesse o endereço do JupyterLab apresentado (Substitua o endereço abaixo pelo que foi exibido em seu terminal):

``` sh
firefox http://127.0.0.1:8888/lab?token=0497e15e042d52cfb498a2edf3d2c6e5874e79b4808ca860
```

**Exemplo de utilização (Docker Compose)**

Abaixo, o mesmo exemplo de execução feito com a `Docker CLI` é realizado com [Docker Compose](https://docs.docker.com/compose/). Para isso, primeiro fez-se a criação do arquivo `docker-compose.yml` com o seguinte conteúdo:

!!! tip "Nome da imagem"

    No comando apresentado abaixo, a Docker Image `research-processing-jupyter` é identificada como `marujore/research-processing-jupyter:latest` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

``` yml title="docker-compose.yml"
version: '3.2'

services:
  my-notebook:

    # Definição do usuário
    user: ${UID}:${GID}
    image: marujore/research-processing-jupyter:latest

    environment:
      # Variáveis de ambiente
      - JUPYTER_ENABLE_LAB=yes
      - DATA_DIRECTORY=/my-data-dir

    volumes:

      # Volume: Volume de dados
      - type: bind
        source: /my-data-dir
        target: /my-data-dir

      # Volume: Volume Daemon Socket
      - type: bind
        source: /var/run/docker.sock
        target: /var/run/docker.sock

    ports:

      # Porta de rede por onde o serviço poderá ser acessado
      - "8888:8888"
```

!!! tip "Definição do usuário"

    Para a definição do usuário, utilizando variáveis de ambiente (`${UID}` e `${GID}`), como apresentado no `docker-compose.yml`, antes de executar o comando `docker-compose`, utilize os seguintes comandos:

    ``` sh
    export UID=`id -u $USER`
    export GID=`cut -d: -f3 < <(getent group docker)`
    ```

Com o arquivo criado, fez-se a execução do compose:

``` sh
docker-compose -f docker-compose.yml up
```

A saída do comando acima deve ser parecida com:

``` sh
# (Omitted)

[I 2022-04-30 19:23:57.260 ServerApp] http://afd0fe2755a7:8888/lab?token=6d37701a6787bd58a7f92f29f33709970df11a742bf3b79b
[I 2022-04-30 19:23:57.260 ServerApp]  or http://127.0.0.1:8888/lab?token=6d37701a6787bd58a7f92f29f33709970df11a742bf3b79b
[I 2022-04-30 19:23:57.260 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2022-04-30 19:23:57.264 ServerApp]

    To access the server, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/jpserver-8-open.html
    Or copy and paste one of these URLs:
        http://afd0fe2755a7:8888/lab?token=6d37701a6787bd58a7f92f29f33709970df11a742bf3b79b
     or http://127.0.0.1:8888/lab?token=6d37701a6787bd58a7f92f29f33709970df11a742bf3b79b
```

Com esta informação, pode-se realizar o acesso ao JupyterLab no navegador. Para isso, abra o link exibido em seu terminal em um navegador:

``` sh
firefox http://127.0.0.1:8888/lab?token=6d37701a6787bd58a7f92f29f33709970df11a742bf3b79b
```

#### Dagster
[![docker-image-type](https://img.shields.io/badge/Type-Environment-orange)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/#)

Para a execução da versão Dagster, fez-se a criação da Docker Image `research-processing-dagster`. Essa Docker Image possui o Dagster (versão `0.12.15`), junto ao [DagIt](https://docs.dagster.io/0.12.15/concepts/dagit/dagit), uma interface web para configurar e interagir com o Dagster. Tem-se também uma instalação do Docker, para que os *scripts* sejam capazes de operar e criar outros Docker Containers de processamento.

**Variáveis de ambiente**

Para a utilização da `research-processing-dagster`, é necessário definir a seguinte variável de ambiente:

`DATA_DIRECTORY` (Obrigatório)

:   Variável de ambiente para determinar o diretório, na máquina local, onde os dados baixados devem ser salvos.

**Volumes**

A execução do `research-processing-dagster` deve ser realizada com a definição dos seguintes volumes `Docker volumes`:

`Volume de dados` (Obrigatório)

:   Volume onde os dados serão armazenados. Seguindo o [modelo de execução](/pt/tools/libraries/#abordagem-de-execucao-das-funcoes) das funções de processamento utilizadas nos *scripts*, esse volume será utilizado por funções dentro do mesmo container (`Local`) ou em outros containers (`Containerized`). Desta forma, a definição desse volume deve ser feita de modo a atender duas exigências:

:     * O volume deve ser do tipo [Bind Mount](https://docs.docker.com/storage/bind-mounts/);
:     * O mapeamento do volume (`Bind Mount`) deve utilizar, na máquina local e no Container, o mesmo caminho definido na variável `DATA_DIRECTORY`.

:   Com essas definições, o volume será visível dentro do Container da `research-processing-dagster` e também pelos Containers auxiliares de processamentos.

`Volume Daemon Socket`

:   Para que os scripts sejam capazes de gerar Docker Containers de processamento, é necessário a definição do [Daemon Socket](https://docs.docker.com/engine/reference/commandline/dockerd/#description) como um volume. Ao fazer isso, o Docker dentro do container criado com a imagem `research-processing-dagster` é capaz de interagir com o Docker da máquina externa, permitindo que containers de processamento sejam criados.

**Exemplo de utilização (Docker CLI)**

Abaixo, faz-se a apresentação de um exemplo de uso da Docker Image `research-processing-dagster` através da Docker CLI:

!!! tip "Nome da imagem"

    No comando apresentado abaixo, a Docker Image `research-processing-dagster` é identificada como `marujore/research-processing-dagster:latest` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

!!! warning "Formatação do comando"

    O comando abaixo é criado para ser ditádico. Caso você queira utiliza-lo, não esqueça de substituir os valores e remover os espaços entre cada linha.


``` sh
docker run \
  --name research-processing-dagster \

  # Variáveis de ambiente
  --env DATA_DIRECTORY=/my-data-dir \

  # Volume: Volume de dados
  --volume /my-data-dir:/my-data-dir \

  # Volume: Volume Daemon Socket
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \

  # Porta de rede por onde o serviço poderá ser acessado
  --publish 3000:3000 \

  # Especificação da Docker Image
  marujore/research-processing-dagster:latest
```

Após a execução do comando acima, um resultado parecido com o apresentado abaixo deve aparecer:

``` sh
  # (Omitted)

  Welcome to Dagster!

  If you have any questions or would like to engage with the Dagster team, please join us on Slack
  (https://bit.ly/39dvSsF).

Serving on http://0.0.0.0:3000 in process 1
```

Após a execução deste comando, utilizando um navegador e acesse o endereço do DagIt apresentado:

``` sh
firefox http://127.0.0.1:3000
```

**Exemplo de utilização (Docker Compose)**

Abaixo, o mesmo exemplo de execução feito com a `Docker CLI` é realizado com [Docker Compose](https://docs.docker.com/compose/). Para isso, primeiro fez-se a criação do arquivo `docker-compose.yml` com o seguinte conteúdo:

!!! tip "Nome da imagem"

    No comando apresentado abaixo, a Docker Image `research-processing-dagster` é identificada como `marujore/research-processing-dagster:latest` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

``` yml title="docker-compose.yml"
version: '3.2'

services:
  my-dagster:
    image: marujore/research-processing-dagster:latest

    environment:
      # Variáveis de ambiente
      - DATA_DIRECTORY=/my-data-dir

    volumes:
      # Volume: Volume de dados
      - type: bind
        source: /my-data-dir
        target: /my-data-dir

      # Volume: Volume Daemon Socket
      - type: bind
        source: /var/run/docker.sock
        target: /var/run/docker.sock

    ports:
      # Porta de rede por onde o serviço poderá ser acessado
      - "3000:3000"
```

Com o arquivo criado, fez-se a execução do compose:

``` sh
docker-compose -f docker-compose.yml up
```

A saída do comando acima é parecida com:

``` sh
  # (Omitted)

  Welcome to Dagster!

  If you have any questions or would like to engage with the Dagster team, please join us on Slack
  (https://bit.ly/39dvSsF).

  Serving on http://0.0.0.0:3000 in process 1
```

Agora, utilizando como base o endereço `http://0.0.0.0:3000` exibido na tela, acesse o Dagster em seu navegador:

``` sh
firefox http://127.0.0.1:3000
```

### Example toolkit environment
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](#)

Para facilitar a utilização do [Example toolkit](/tools/utilitary/#example-toolkit), fez-se a criação da Docker Image `example-toolkit-docker`. Esta Docker Image, possui todas as dependências necessárias para a execução do `Example toolkit`.

Nos tópicos abaixo, é feita a apresentação das configurações necessárias para utilizar essa Docker Image. Exemplos de utilização com a CLI do Docker e [Docker Compose](https://docs.docker.com/compose/), também serão apresentados.

**Variáveis de ambiente**

Na utilização do `Example toolkit`, toda a configuração é feita através de variáveis de ambiente. Na `example-toolkit-docker`, manteve-se o mesmo padrão. Sendo assim, antes de realizar a execução dessa Image, deve-se definir as variáveis de ambiente obrigatórias. As mesmas variáveis de ambiente válidas para o `Example toolkit` são válidas para a `example-toolkit-docker`.

Para verificar a lista completa das variáveis de ambiente do `Example toolkit`, juntamente com a explicação de cada uma delas, consulte a Seção [Example toolkit - Utilização](/pt/tools/utilitary/#utilizacao).

**Volumes**

Para a utilização da `example-toolkit-docker`, é necessário a definição de alguns Docker Volumes. Esses volumes, especificam os dados de entrada, saída, configurações e dados auxiliares. Abaixo, tem-se a apresentação de cada um desses volumes:

`Volume de dados` (Obrigatório)

:   Diretório onde os dados baixados serão armazenados. Esse volume precisa ser criado no mesmo diretório definido na variável de ambiente `DOWNLOAD_OUTPUT_DIRECTORY` (Configuração do `Example toolkit`).

`Volume de configuração Dagster` (Obrigatório)

:   Diretório onde o arquivo de configuração Dagster gerado será salvo. Esse volume precisa ser criado no mesmo diretório definido na variável de ambiente `PIPELINE_DIR` (Configuração do `Example toolkit`).

`Volume de configuração do download` (Obrigatório)

:   Arquivo de configuração com a referência aos dados que precisam ser baixado. O arquivo definido nesse volume deve ser o mesmo especificado na variável `DOWNLOAD_REFERENCE_FILE` (Configuração do `Example toolkit`).

**Exemplo de utilização (Docker CLI)**

Abaixo, faz-se a execução da Docker Image, identificada com a tag `example-toolkit-docker`:

!!! tip "Nome da imagem"

    No comando apresentado abaixo, a Docker Image `example-toolkit-docker` é identificada como `marujore/example-toolkit-docker:latest` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

!!! warning "Formatação do comando"

    O comando abaixo é criado para ser ditádico. Caso você queira utiliza-lo, não esqueça de substituir os valores e remover os espaços entre cada linha.

``` sh
docker run \
  --name example-toolkit-docker \

  # Variáveis de ambiente
  --env RAW_DATA_DIR=/compendium/data/raw_data \
  --env DERIVED_DATA_DIR=/compendium/data/derived_data \
  --env PIPELINE_DIR=/compendium/config \
  --env DOWNLOAD_OUTPUT_DIRECTORY=/compendium/data \
  --env DOWNLOAD_REFERENCE_FILE=/compendium/config/example-toolkit.json \

  # Volume: Volume de dados
  --volume /my-data/dir:/compendium/data \

  # Volume: Volume de configuração Dagster
  --volume /my-dagster/dir:/compendium/config \

  # Volume: Volume de configuração do download
  --volume /my-toolkit/config.json:/compendium/config/example-toolkit.json \

  # Especificação da Docker Image
  marujore/example-toolkit-docker:latest
```

Após a execução do comando acima, deverá ser produzir um resultado parecido com o apresentado abaixo:

``` sh
# (Omitted)

2022-04-30 14:59:16.525 | INFO     | pipeline_steps:download_data_files_from_github:59 - Downloading minimal-example_landsat8_data.zip (Sometimes the progress bar may not appear. Please, be patient.)
100%|██████████████████████████████████████████████████████████| 2.05G/2.05G [03:43<00:00, 9.17MB/s]
2022-04-30 15:03:32.059 | INFO     | pipeline_steps:download_data_files_from_github:59 - Downloading minimal-example_lasrc_auxiliary_data.zip (Sometimes the progress bar may not appear. Please, be patient.)
100%|████████████████████████████████████████████████████████████| 341M/341M [00:35<00:00, 9.57MB/s]
2022-04-30 15:04:44.977 | INFO     | pipeline_steps:download_data_files_from_github:59 - Downloading minimal-example_scene_id_list.zip (Sometimes the progress bar may not appear. Please, be patient.)
100%|██████████████████████████████████████████████████████████| 2.17k/2.17k [00:00<00:00, 1.16MB/s]
2022-04-30 15:04:45.690 | INFO     | pipeline_steps:download_data_files_from_github:59 - Downloading minimal-example_sentinel2_data.zip (Sometimes the progress bar may not appear. Please, be patient.)
100%|██████████████████████████████████████████████████████████| 1.14G/1.14G [02:12<00:00, 8.59MB/s]
2022-04-30 15:07:15.765 | INFO     | pipeline_steps:download_data_files_from_github:92 - All files are downloaded.
```

**Exemplo de utilização (Docker Compose)**

Abaixo, o mesmo exemplo de execução feito com a `Docker CLI` é realizado com [Docker Compose](https://docs.docker.com/compose/). Para isso, primeiro fez-se a criação do arquivo `docker-compose.yml` com o seguinte conteúdo:

!!! tip "Nome da imagem"

    No comando apresentado abaixo, a Docker Image `example-toolkit-docker` é identificada como `marujore/example-toolkit-docker:latest` já que esta, está armazenada no perfil de usuário [marujore](https://hub.docker.com/u/marujore) no DockerHub e a versão escolhida é a `latest`.

``` yml title="docker-compose.yml"
version: '3.2'

services:
  my-dagster:
    # Especificação da Docker Image
    image: marujore/example-toolkit-docker:latest

    environment:
      # Variáveis de ambiente
      - RAW_DATA_DIR=/compendium/data/raw_data
      - DERIVED_DATA_DIR=/compendium/data/derived_data
      - PIPELINE_DIR=/compendium/config
      - DOWNLOAD_OUTPUT_DIRECTORY=/compendium/data
      - DOWNLOAD_REFERENCE_FILE=/compendium/config/example-toolkit.json

    volumes:
      # Volume: Volume de dados
      - type: bind
        source: /my-data/dir
        target: /compendium/data

      # Volume: Volume de configuração Dagster
      - type: bind
        source: /my-dagster/dir
        target: /compendium/config

      # Volume: Volume de configuração do download
      - type: bind
        source: /my-toolkit/config.json
        target: /compendium/config/example-toolkit.json

    ports:
      # Porta de rede por onde o serviço poderá ser acessado
      - "3000:3000"
```

Com o arquivo criado, fez-se a execução do compose:

``` sh
docker-compose -f docker-compose.yml up
```

A saída do comando acima é parecida com:

``` sh
  # (Omitted)

  Welcome to Dagster!

  If you have any questions or would like to engage with the Dagster team, please join us on Slack
  (https://bit.ly/39dvSsF).

  Serving on http://0.0.0.0:3000 in process 1
```

## Máquina virtual com Vagrant  <img src="/assets/tools/environment/vagrant/vagrant-logo.png" align="right" width="160"/>

Todos os recursos disponibilizados neste RC, foram desenvolvidos, testados e utilizados em ambiente `Linux`. Especificamente, fez-se o uso do `Ubuntu 20.04`. Testes com o `Ubuntu 20.10` também foram realizados. Em teoria, os códigos executados, podem ser adaptados e utilizados em outros sistemas operacionais, como `Windows` e `MacOS`.

No entanto, é importante notar que, não existe uma garantia de que todos os comandos, configurações e dependências utilizadas estarão disponíveis para outros ambientes. Mesmo com o uso do Docker, pode ser que características específicas utilizadas, como os [Daemon Socket](https://docs.docker.com/engine/reference/commandline/dockerd/#description), não estejam disponíveis.

Para resolver este problema e evitar que o sistema operacional seja uma barreira para a reprodução e replicação do material deste RC, fez-se a criação de uma Máquina Virtual (VM, do inglês *Virtual Machine*). Com uma VM, diferente do Docker, tem-se a virtualização de um sistema completo, o que remove qualquer dependência com o sistema adjacente.

A criação dessa VM, foi realizada com o auxílio do [Vagrant](https://www.vagrantup.com/), uma ferramenta que facilita o gerenciamento e provisionamento de máquinas virtuais, desenvolvida pela [Hashicorp](https://www.hashicorp.com/). Vagrant está disponível para Windows, Linux, MacOS e outros sistemas operacionais. Com essa ferramenta, através de um arquivo de descrição ([Vagrantfile](https://www.vagrantup.com/docs/vagrantfile)), é possível especificar uma VM completa, considerando elementos como:

* Quantidade de memória RAM;
* Quantidade de CPU;
* Sistema operacional;
* Rede;
* Pacotes instalados.

Além dessas, muitas outras configurações estão disponíveis.

Utilizando dessas características, neste RC, fez-se a criação de um `Vagrantfile` que especifica uma VM `Ubuntu 20.04`, já preparada com as principais dependências necessárias para uso dos materiais deste RC (e.g., Docker, Docker Compose). Por padrão, a máquina é criada com `12 GB` de RAM e `8 CPUs`.

!!! note "Recursos da VM"

    A quantidade de recursos definida para a VM foi feita considerando como base uma máquina de 24 GB de RAM e 12 CPUs. Caso seja necessário, através do `Vagrantfile`, esses valores podem ser alterados. Para isso, altere as seguintes propriedades disponíveis no arquivo:

    ``` yml
    vb.memory = "12288"  # 12 GB

    vb.cpus = "8"
    ```

O Vagrant suporta vários [Providers](https://www.vagrantup.com/docs/providers), que são as ferramentas utilizadas para criar as VMs. Neste RC, fez-se o uso do Provider Open Source [VirtualBox](https://www.virtualbox.org/).


### Instalação do Vagrant

Para começar a utilizar a VM através do Vagrant, o primeiro passo é realizar a instalação do Vagrant propriamente dito. Para isso, recomenda-se a utilização da [documentação oficial](https://www.vagrantup.com/docs/installation).

### Utilização da VM via Vagrant

Uma vez que o Vagrant está instalado em seu sistema, para a criação da VM, o primeiro passo é realizar o clone do repositório onde estão todos os materiais deste RC:

``` sh
git clone https://github.com/marujore/compendium-harmonization
```

Após o clone, acesse o diretório `compendium-harmonization`:

``` sh
cd compendium-harmonization
```

Dentro do repositório, você será capaz de ver todos os materiais deste RC:

``` sh
ls -lha

#> -rwxrwxrwx 1 felipe felipe  368 Apr  9 20:01 .dockerignore
#> drwxrwxrwx 1 felipe felipe  512 Apr 14 17:00 .git
#> drwxrwxrwx 1 felipe felipe  512 Apr 15 22:53 .github
#> -rwxrwxrwx 1 felipe felipe 4.3K Apr 10 08:42 .gitignore
#> -rwxrwxrwx 1 felipe felipe 1.1K Apr  9 20:01 LICENSE
#> -rwxrwxrwx 1 felipe felipe 2.7K Apr 30 18:38 Makefile
#> -rwxrwxrwx 1 felipe felipe 4.5K Apr  9 20:01 README.md
#> -rwxrwxrwx 1 felipe felipe 3.4K Apr 15 22:53 Vagrantfile
#> drwxrwxrwx 1 felipe felipe  512 Apr 14 17:00 analysis
#> -rwxrwxrwx 1 felipe felipe 1.4K Apr 10 08:19 bootstrap.sh
#> drwxrwxrwx 1 felipe felipe  512 Apr 14 17:00 composes
#> drwxrwxrwx 1 felipe felipe  512 Apr 14 17:00 docker
#> -rwxrwxrwx 1 felipe felipe  383 Apr 10 07:39 setenv.sh
#> drwxrwxrwx 1 felipe felipe  512 Apr 14 17:00 tools
```

Dentre esses arquivos, note que há disponível o arquivo `Vagrantfile`. Esse arquivo, como citado anteriormente, tem toda a especificação da VM que deve ser criada. Para criar a VM com esse arquivo, utilize o seguinte comand:


``` sh
vagrant up

#> Bringing machine 'default' up with 'virtualbox' provider...
#> ==> default: Checking if box 'alvistack/ubuntu-20.04' version '20220415.1.1' is up to date...
#> ==> default: A newer version of the box 'alvistack/ubuntu-20.04' for provider 'virtualbox' is
#> ==> default: available! You currently have version '20220415.1.1'. The latest is version
#> ==> default: '20220430.1.2'. Run `vagrant box update` to update.
#> ==> default: Resuming suspended VM...
#> ==> default: Booting VM...
#> ==> default: Waiting for machine to boot. This may take a few minutes...
#>     default: SSH address: 127.0.0.1:2222
#>     default: SSH username: vagrant
#>     default: SSH auth method: private key
```

Após a execução desse arquivo, a VM já estará criada e pronta para ser utilizada. Neste caso, para acessar a VM, utilize o comando:

``` sh
vagrant ssh

#> Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.13.0-39-generic x86_64)

#>  * Documentation:  https://help.ubuntu.com
#>  * Management:     https://landscape.canonical.com
#>  * Support:        https://ubuntu.com/advantage

 # (Omitted)

#> vagrant@ubuntu:~$
```

Ao acessar o ambiente, você está pronto para utilizar os materiais disponibilizados neste RC. Por exemplo, caso você queira acessar os materiais do RC que você fez o clone para criar a VM, você pode acessar o diretório `/compendium`:

*Mudando de diretório*
``` sh
cd /compendium
```

*Listando os arquivos*
``` sh
ls -lha

#> drwxrwxrwx  1 vagrant vagrant    0 Apr 14 20:00 analysis
#> -rwxrwxrwx  1 vagrant vagrant 1.4K Apr 10 11:19 bootstrap.sh
#> drwxrwxrwx  1 vagrant vagrant    0 Apr 14 20:00 composes
#> drwxrwxrwx  1 vagrant vagrant    0 Apr 14 20:00 docker
#> -rwxrwxrwx  1 vagrant vagrant  368 Apr  9 23:01 .dockerignore
#> -rwxrwxrwx  1 vagrant vagrant   17 Apr 10 11:25 .env
#> drwxrwxrwx  1 vagrant vagrant    0 Apr 16 01:53 .github
#> -rwxrwxrwx  1 vagrant vagrant 4.3K Apr 10 11:42 .gitignore
#> -rwxrwxrwx  1 vagrant vagrant 1.1K Apr  9 23:01 LICENSE
#> -rwxrwxrwx  1 vagrant vagrant 2.7K Apr 30 21:38 Makefile
#> -rwxrwxrwx  1 vagrant vagrant 4.5K Apr  9 23:01 README.md
#> -rwxrwxrwx  1 vagrant vagrant  383 Apr 10 10:39 setenv.sh
#> drwxrwxrwx  1 vagrant vagrant 4.0K Apr 14 20:00 tools
#> drwxrwxrwx  1 vagrant vagrant    0 May  1 19:16 .vagrant
#> -rwxrwxrwx  1 vagrant vagrant 3.4K Apr 16 01:53 Vagrantfile
```
