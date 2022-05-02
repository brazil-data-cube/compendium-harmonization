<!-- Abbreviations -->
*[RC]: Research Compendium

# Scripts de processamento

Para a implementação da metodologia dos experimentos realizados neste RC, inicialmente fez-se a criação de um [conjunto de bibliotecas de software](/pt/tools/libraries). Com base nessas bibliotecas e todas as funcionalidades que essas disponibilizam, nós realizamos a implementação de *scripts* de processamento. Esses *scripts* representam a materialização da metodologia dos experimentos realizados neste RC.

Esses *scripts* de processamento, foram implementados utilizando duas ferramentas:

[Jupyter Notebook](https://jupyter.org/): Ambiente de computação interativa, que permitem a criação de notebooks computacionais que implementam os conceitos de computação letrada, o qual permite a mescla de textos e código em um mesmo documento;

[Dagster](https://docs.dagster.io/0.12.15/getting-started): Plataforma que permite a criação, gerenciamento e execução de fluxos de processamento e manipulação de dados.

Ambas implementações listadas acima, utilizam as mesmas bibliotecas e versões para a realização do processamento, garantindo a produção de resultados reprodutíveis e comparáveis. A escolha pela implementação do fluxo de processamento em duas ferramentas distintas foi realizada por alguns motivos, sendo os principais deles listados abaixo:

1. Apresentação das capacidades de uso das biblioteca criadas neste RC;
2. Abrangência nos cenários de uso da metodologia implementada neste RC;
3. Dupla implementação, o que permite a comparação dos resultados gerados de diferentes formas, partindo das mesmas ferramentas.

De forma geral, a ligação de cada um desses *scripts* de processamento e as [bibliotecas de software](/pt/tools/libraries) desenvolvidas nesse RC, são apresentadas na Figura abaixo:

<figure markdown>
  ![libs-link](/assets/tools/processing/processing-scripts-libs-overview.svg){ width="1024" }
  <figcaption>Relação entre as bibliotecas de funcionalidades e <i>scripts</i> de processamento.</figcaption>
</figure>

## Jupyter Notebook

Por vezes, quando a metodologia implementada está sendo explorado, por exemplo, em cenários de desenvolvimento, é necessário que todos os passos sejam bem documentos e organizados de forma clara. Para esse tipo de cenário, foi realizada a implementação da metodologia deste RC utilizando o Jupyter Notebook.

No Jupyter Notebook implementado, todas as etapas são documentadas e descritas, de modo que todos possam explorar e enteder o que está sendo realizado. No vídeo abaixo, tem-se a apresentação de algumas partes desse notebook.

<figure markdown>
  ![libs-link](/assets/tools/processing/jupyter/jupyter-notebook-overview.gif){ width="1024" }
  <figcaption>Exemplo de parte do Jupyter Notebook de processamento.</figcaption>
</figure>

### Configurações

Para a utilização desse Jupyter Notebook é necessário apenas uma configuração: A definição da variável de ambiente `DATA_DIRECTORY`. Essa variável de ambiente, determina o local onde está o diretório de dados que deverá ser utilizado pelo notebook para carregar os dados de entrada e salvar os resultados gerados. 

!!! tip "Sobre o diretório de dados"

    Os detalhes de como o diretório de dados definido na variável de ambiente `DATA_DIRECTORY` deve estar organizado são apresentados na seção [Diretório de dados](#diretorio-de-dados).

## Dagster

!!! warning "Sobre a versão do Dagster"

    No momento em que esse RC estava sendo construído, a versão oficial do Dagste era `0.12.15`. Atualmente, as versões mudaram, o que trouxe novas nomenclaturas e definições ao *software*. Para manter o conteúdo consistente, as explicações utilizadas nessa documentação, foram criadas com base na versão `0.12.15`.

!!! warning "Nomenclaturas"

    No Dagster, todo fluxo de processamento criado é chamado de **Pipeline**. Neste documento, para manter a consistência com as explicações realizadas com o Jupyter Notebook, os pipelines serão genericamente tratados como *scripts* de processamento.

    Caso você deseje, pode consultar a [documentação oficial do Dagster (v0.12.15)](https://docs.dagster.io/0.12.15/getting-started) onde tem-se uma explicação detalhada do que são os [Pipelines](https://docs.dagster.io/0.12.15/concepts/solids-pipelines/pipelines).

Com a metodologia implementada e pronta para ser utilizada, sua execução com o uso de grandes volumes de dados pode exigir diversos controles e ações como:

1. Execução paralela das operações;
2. Controle de falhas;
3. Reexecução.

Com base nessa necessidade, foi criado o *script* de processamento utilizando a ferramenta [Dagster](https://docs.dagster.io/0.12.15/getting-started). Com essa ferramenta, toda a orquestração da operação pode ser feita de maneira simples e direta. Além disso, quando necessário e devidamente configurado, diferentes formas de execução podem ser adotados, como execuções distribuídas, paralelas. Outro ponto possitivo ao uso do Dagster está no controle de falhas e reexecução.

A criação do *script* de processamento é feita utilizando uma interface de programação (API) em linguagem Python, no entanto, a manipulação e uso do *script* é feita através de uma interface *web*. Nessa interface, tem-se disponível opções para executar o processamento, fazer seu gerenciamento, bem como consultar a documentação de cada uma das etapas e ver o fluxo geral que é realizado. O vídeo abaixo, apresenta uma visão geral dessa interface:

<figure markdown>
  ![libs-link](/assets/tools/processing/dagster/dagster-overview.gif){ width="1024" }
  <figcaption>Exemplo de parte da interface do Dagster com a visão do fluxo de processamento.</figcaption>
</figure>

### Configurações

Para realizar a execução do *script* de processamento criado com o Dagster, é necessário realizar a configuração da ferramenta. Essa configuração é feita através da definição de parâmetros em um arquivo no formato `YAML`, o qual especifica:

1. Onde os dados de entrada estão armazenados;
2. Qual será o diretório de saída;
3. Quais imagens e bandas espectrais devem ser utilizadas;
4. Especificação de recursos computacionais (e.g., Quantidade de CPU utilizada).

Esse arquivo, uma vez criado, é inserido na interface do Dagster, onde é feita sua validação e uso para a criação de uma nova execução do *script*. 

!!! tip "Sobre execuções no Dagster"

    Para saber mais detalhes sobre como o Dagster realiza a criação de suas execuções na versão `0.12.15`, por favor, consulte a [documentação oficial da ferramenta](https://docs.dagster.io/0.12.15/concepts/configuration/config-schema#config-schema)

Para que você seja capaz de criar configurações do Dagster para realizar execuções com seus próprios dados e necessidades, nas subseções abaixo faz-se a apresentação da estrutura do arquivo de configuração `YAML` do Dagster. 

#### Arquivo de configuração Dagster

O arquivo de configuração Dagster, como mencionado anteriormente, é utilizado para definir os recursos que serão utilizados durante a execução do *script* de processamento. Esse arquivo de configuração, no formato `YAML`, é dividido em duas principais seções: (i) Resources; (ii) Solids. Cada uma dessas seções, é responsável por realizar uma parte da configuração, de modo a permitir que as definições mencionadas anteriormente possam ser realizadas. Cada seção e as configurações definidas são apresentadas nos tópicos a seguir

!!! tip "Sobre o arquivo de configuração"

    Ao utilizar o Jupyter Notebook, toda a configuração é feita através de uma única variável de ambiente (`DATA_DIRECTORY`). No Dagster, o arquivo de configuração tem exatamente o mesmo papel.

    Sendo assim, é recomendado que antes de você acompanhar os tópicos de definição do arquivo de configuração, você consulte a seção [Diretório de dados](#diretorio-de-dados), na qual é especificado a estrutura de diretórios que deve ser seguida, bem como o conteúdo que deve estar disponível em cada seção.

##### Resources

No Dagster, [resources](https://docs.dagster.io/0.12.15/concepts/modes-resources#overview) são utilizados para representar elementos e recursos do ambiente computacional que **devem** estar disponíveis para a execução do *script* de processamento. No caso do *script* de processamento desse RC, os *resources* representam os dados que devem ser utilizados durante o processamento. Sendo assim, a um *resource*, pode-se ter associado um ou mais diretórios de dados. Ao todo, o *script* de processamento necessita de dois *resources*:

**lasrc_data**

*Resource* onde tem-se a disponibilização de dados relacionados a ferramenta LaSRC. A definição de um *resource* `lasrc_data` requer a especificação da seguinte variável de configuração:

`lasrc_auxiliary_data_dir`: Variável onde faz-se a definição do caminho para o diretório de dados auxiliares da ferramente LaSRC, requeridos para a realização da correção atmosférica em imagens Sentinel-2/MSI. 


!!! info "Organização do diretório de dados"
    
    Para mais detalhes de como esse diretório de dados auxiliares deve ser organizado, por favor, consulte a seção [Diretório de dados](#diretorio-de-dados).

Um exemplo completo de definição de um *resource* `lasrc_data` é apresentado abaixo:

```yaml
resources:
  lasrc_data:
    config:
      lasrc_auxiliary_data_dir: /path/to/lasrc/auxiliary/data
```

Esse bloco de código deve ser definido dentro do arquivo de configuração. Para um exemplo completo, consulte o [arquivo de configuração do dagster](#full-example).

**repository**

*Resource* onde faz-se a definição dos diretórios de entrada e saída do *script* de processamento. A definição de um *resource* `repository` requer a especificação das seguintes variáveis de configuração:

`landsat8_input_dir`: Diretório onde estão disponíveis os dados Landsat-8/OLI, que podem ser utilizados como entrada para o *script* de processamento;

`sentinel2_input_dir`: Diretório onde estão disponíveis os dados Sentinel-2/MSI, que podem ser utilizados como entrada para o *script* de processamento;

`derived_data_dir`: Diretório onde os dados gerados durante as etapas de processamento serão salvos.

!!! info "Organização do diretório de dados"

    Para mais detalhes de como cada um desses diretórios devem ser organizados, por favor, consulte a seção [Diretório de dados](#diretorio-de-dados).

Um exemplo completo de definição de um *resource* `repository` é apresentado abaixo:

```yaml
resources:
  repository:
    config:
      derived_data_dir: /path/to/derived/data/dir
      landsat8_input_dir: /path/to/input/landsat8/data/dir
      sentinel2_input_dir: /path/to/input/sentinel2/data/dir 
```

Esse bloco de código deve ser definido dentro do arquivo de configuração. Para um exemplo completo, consulte o [arquivo de configuração do dagster](#full-example).

##### Solids

No Dagster, [solids](https://docs.dagster.io/0.12.15/concepts/solids-pipelines/solids#solids) representam a unidade funcional de trabalho que fará a execução de uma operação de fato. Esses elementos são os responsáveis por receber as entradas, realizar um processamento e gerar as saídas. Assim, no *script* de processamento, eles foram utilizados para representar cada uma das etapas de processamento.

Os **solids** podem ou não requerer algum tipo de configuração para sua definição. No caso do *script* de processamento deste RC, apenas um deles necessita de configuração, sendo ele:

`load_and_standardize_sceneids_input`: *solid* responsável em receber os arquivos com a definição das cenas Landsat-8/OLI e Sentinel-2/MSI que deverão ser processadas. Ao receber esses arquivos, o *solid* faz a leitura, validação e então passa as informações carregadas para as etapas subsequentes, que as utilizam para a realização das atividades de processamento. Na configuração desse *solid*, faz-se necessário a especificação das seguintes variáveis de configuração:

- `landsat8_sceneid_list`: Arquivo `.txt` com o nome das cenas Landsat-8/OLI que deverão ser consideradas no fluxo de processamento. Esses nomes devem ser o mesmo disponível no diretório de dados Landsat-8/OLI (`landsat8_input_dir`) especificado no *resource* `repository`;

- `sentinel2_sceneid_list`: Arquivo `.txt` com o nome das cenas Sentinel-2/MSI que deverão ser consideradas no fluxo de processamento. Esses nomes devem ser o mesmo disponível no diretório de dados Sentinel-2/MSI (`sentinel2_input_dir`) especificado no *resource* `repository`;

!!! info "Organização do diretório de dados"

    Para mais detalhes de como os arquivos com os nomes das cenas devem estar organizados, por favor, consulte a seção [Diretório de dados](#diretorio-de-dados).

Um exemplo completo de definição de um *solid* `load_and_standardize_sceneids_input` é apresentado abaixo:

```yaml
solids:
  load_and_standardize_sceneids_input:
    config:
      landsat8_sceneid_list: /path/to/input/landsat8/data/landsat.txt
      sentinel2_sceneid_list: /path/to/input/sentinel2/data/sentinel.txt
```

##### Exemplo completo

Abaixo, faz-se a apresentação de um arquivo completo de configuração Dagster, que utiliza todos os *resources* e *solids* especificados nos tópicos anteriores:

Para exemplificar todos os elementos citados anteriormente em um arquivo de configuração, abaixo é apresentado a configuração mínima necessária para a execução do pipeline deste RC.

```yaml
resources:
  lasrc_data:
    config:
      lasrc_auxiliary_data_dir: /path/to/lasrc/auxiliary/data
  repository:
    config:
      derived_data_dir: /path/to/derived/data/dir
      landsat8_input_dir: /path/to/input/landsat8/data/dir
      sentinel2_input_dir: /path/to/input/sentinel2/data/dir 

solids:
  load_and_standardize_sceneids_input:
    config:
      landsat8_sceneid_list: /path/to/input/landsat8/data/landsat.txt
      sentinel2_sceneid_list: /path/to/input/sentinel2/data/sentinel.txt
```

## Diretório de dados

Em ambas as implementações dos *scripts* de processamento, na etapa de configuração, faz-se necessário a definição do caminho para o diretório de dados. Esse diretório possui uma organização padrão, de modo que, independente da forma com que a execução será realizada, a mesma organização de dados pode ser seguida. Nesta seção, será apresentado o formato de organização desse diretório de dados. Para começar, primeiro é importante entender que:

!!! quote ""

    O diretório de dados, utilizado em ambos *scripts* de processamento, representam o diretório de entradas e saídas do *script*. Todas as entradas são lidas desse diretórios, não sendo possível ler dados de diferentes diretórios. O mesmo vale para as saídas, os resultados produzidos sempre serão armazenados em nesse diretório.

A lógica por trás da definição desse diretório é a da organização: Se o pesquisador precisa centralizar e manter organizado em uma estrutura lógica todos os materiais que ele está utilizando para produzir os resultados, bem como os resultados propriamente ditos, ele minimamente terá de manter seus objetos de pesquisa organizados.

Para que esse diretório suporte toda essas utilidades, diferentes subdiretórios são criados abaixo dele. Nesses diretórios tem-se a definição dos dados de entrada e saída. Abaixo, a estrutura do diretório de dados, esperada por ambos os *scripts* de processamento serão apresentados:

    data directory
        ├── derived_data
        └── raw_data
            ├── landsat8_data
            ├── sentinel2_data
            ├── scene_id_list
            └── lasrc_auxiliary_data

Onde:

**raw_data**

Diretório onde os dados de entrada devem ser armazenados. Os subdiretório desse, são explicados abaixo.

**raw_data/landsat8_data**

Nesse diretório, devem ser colocados todos os dados Landsat-8/OLI que podem ser utilizados como entrada nos *scripts* de processamento. Para o caso do Landsat-8/OLI, é esperado que as imagens estejam separadas por diretórios. Abaixo, é apresentado a estrutura desse diretório:

```
landsat8_data
    ├── LC08_L2SP_222081_20171120_20200902_02_T1
    └── LC08_L2SP_223081_20171111_20200902_02_T1
```

A organização das imagens dentro de cada diretório, deve seguir o formato utilizado pela **U**nited **S**tates **G**eological **S**urvey (USGS) na distribuição dos dados L2 (com correção atmosférica). Além disso, a nomenclatura do diretório, também deve seguir o padrão de disseminação da USGS. Caso esse padrão não seja seguido, erros podem surgir durante as etapas de processamento.

Abaixo, tem um exemplo de como esse diretório deve estar organizado internamente:

```
landsat8_data
    └── LC08_L2SP_223081_20171111_20200902_02_T1
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ANG.txt
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_MTL.json
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_MTL.txt
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_MTL.xml
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_QA_PIXEL.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_QA_RADSAT.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_B1.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_B2.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_B3.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_B4.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_B5.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_B6.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_B7.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_QA_AEROSOL.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_SR_stac.json
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_ATRAN.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_B10.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_CDIST.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_DRAD.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_EMIS.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_EMSD.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_QA.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_stac.json
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_TRAD.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_ST_URAD.TIF
        ├── LC08_L2SP_223081_20171111_20200902_02_T1_thumb_large.jpeg
        └── LC08_L2SP_223081_20171111_20200902_02_T1_thumb_small.jpeg
```

**raw_data/sentinel2_data**

Nesse diretório, devem ser colocados todos os dados Sentinel-2/MSI que podem ser utilizados como entrada nos *scripts* de processamento. Para o caso do Sentinel-2/MSI, é esperado que as imagens estejam separadas por diretórios. Abaixo, é apresentado a estrutura desse diretório:

```
sentinel2_data
    ├── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
    └── S2B_MSIL1C_20171122T134159_N0206_R124_T22JBM_20171122T200800.SAFE
```

A organização das imagens dentro de cada diretório, deve seguir o formato dos diretórios `.SAFE` disponibilizados pela USGS. Deve-se notar que, a nomenclatura do diretório, também deve seguir o padrão de disseminação da USGS (Incluindo o `.SAFE`). Caso esse padrão não seja seguido, erros podem surgir durante as etapas de processamento.

Abaixo, tem um exemplo de como esse diretório deve estar organizado internamente:

```
sentinel2_data
    └── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
        ├── AUX_DATA
        ├── DATASTRIP
        ├── GRANULE
        ├── HTML
        ├── INSPIRE.xml
        ├── manifest.safe
        ├── MTD_MSIL1C.xml
        ├── rep_info
        └── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608-ql.jpg
```

**raw_data/scene_id_list**

Diretório onde estão os arquivos de definição de quais dados, daqueles que estão disponíveis nos diretórios `landsat8_data` e `sentinel2_data`, devem ser considerados nas etapas de processamento. Para isso, nesse diretório tem-se dois arquivos:

`scene_ids_lc8.txt`: Arquivo de definição de quais imagens Landsat-8/OLI do diretório (`landsat8_data`) devem ser processados;
`scene_ids_s2.txt`: Arquivo de definição de quais imagens Sentinel-2/MSI do diretório (`sentinel2_data`) devem ser processados.

Em ambos os arquivos, deve-se definir o nome dos diretórios das imagens que devem ser consideradas nas etapas de processamento. Para exemplificar sua utilização, considere os seguintes diretórios `landsat8_data` e `sentinel2_data`:

```
landsat8_data
    ├── LC08_L2SP_222081_20171120_20200902_02_T1
    └── LC08_L2SP_223081_20171111_20200902_02_T1

sentinel2_data
    ├── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
    └── S2B_MSIL1C_20171122T134159_N0206_R124_T22JBM_20171122T200800.SAFE
```

Para que esses dados sejam considerados nos *scripts* de processamento, os arquivos de definição devem ser preenchidos da seguinte forma:

*scene_ids_lc8.txt*

```
LC08_L2SP_222081_20171120_20200902_02_T1
LC08_L2SP_223081_20171111_20200902_02_T1
```

*scene_ids_s2.txt*

```
S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
S2B_MSIL1C_20171122T134159_N0206_R124_T22JBM_20171122T200800.SAFE
```

Os diretórios que não são listados nesses arquivos, não são considerados nas etapas de processamento.

**raw_data/lasrc_auxiliary_data**

Nesse diretório, devem estar armazenados os dados auxiliares utilizados na aplicação do LaSRC. A organização do diretório deve ser a mesma utilizada no [FTP de disseminação USGS](https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/) da USGS. Abaixo, tem-se um exemplo de organização:

```
lasrc_auxiliary_data
    ├── CMGDEM.hdf
    ├── LADS
    ├── LDCMLUT
    ├── MSILUT
    └── ratiomapndwiexp.hdf
```

Deve-se notar que para o fluxo de processamento, apenas os arquivos do diretório `lasrc_auxiliary_data/LADS` devem ser alterados. Nesse diretório, os arquivos equivalentes as imagens Sentinel-2/MSI que serão processadas devem estar disponíveis. Para exemplificar, considere o diretório `sentinel2_data` abaixo:

```
sentinel2_data
    ├── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
    └── S2B_MSIL1C_20171122T134159_N0206_R124_T22JBM_20171122T200800.SAFE
```

Para que todas as imagens desse diretório sejam processadas com o LaSRC durante a execução dos *scripts* de processamento, os seus respectivos arquivos `LADS` devem estar definidos. Nesse caso:

```
lasrc_auxiliary_data
    ├── CMGDEM.hdf
    └── LADS
       └── 2017
           ├── L8ANC2017315.hdf_fused
           ├── L8ANC2017323.hdf_fused
           └── L8ANC2017326.hdf_fused
```

**derived_data**

Diretório onde os resultados gerados serão armazenados. Ao final da execução do *script* de processamento, esse diretório terá a seguinte estrutura:

```
derived_data
    ├── l8
    │   ├── lc8_nbar_angles
    │   └── lc8_nbar
    └── s2
        ├── s2_lasrc_sr
        ├── s2_lasrc_nbar
        ├── s2_sen2cor_sr
        └── s2_sen2cor_nbar
```

Onde:

*Landsat-8/OLI data*

- `l8/lc8_nbar_angles`: Bandas de ângulos geradas para os dados Landsat-8/OLI;

- `l8/lc8_nbar`: Produtos NBAR gerados com dados Landsat-8/OLI.

*Sentinel-2/MSI LaSRC data*

- `s2/s2_lasrc_sr`: Dados Sentinel-2/MSI com correção atmosférica feita através da ferramenta LaSRC;

- `s2/s2_lasrc_nbar`: Produtos NBAR gerados com dados Sentinel-2/MSI com correção atmosférica feita através da ferramenta LaSRC (O mesmo diretório `s2/s2_lasrc_sr`).

*Sentinel-2/MSI Sen2Cor data*

- `s2/s2_sen2cor_sr`: Dados Sentinel-2/MSI com correção atmosférica feita através da ferramenta Sen2Cor;

- `s2/s2_sen2cor_nbar`: Produtos NBAR gerados com dados Sentinel-2/MSI com correção atmosférica feita através da ferramenta Sen2Cor (O mesmo diretório `s2/s2_sen2cor_sr`).
