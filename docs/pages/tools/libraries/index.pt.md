*[RC]: Research Compendium
*[SAA]: Solar Azimutal
*[SZA]: Solar Zenital
*[VAA]: Sensor Azimutal
*[VZA]: Sensor Zenital

# Bibliotecas de software

A reprodutibilidade nos permite refazer o caminho que foi trilhado originalmente para a obtenção dos resultados de uma pesquisa científica. Com isso, outros pesquisadores e mesmo nossos próprios "eus" do futuro podem se beneficiar e entender o que fizemos. Isso da margem para que possíveis erros sejam facilmente detectados e corrigidos.

Dentre as várias ações que podem ser realizadas para atingir a reprodutibilidade, está a capacidade de automatizar os passos já realizado. Isso trás uma série de benefícios, dentre eles:

1. Evita possíveis "erros" por leitura de resultados incorretos que não são mais válidos para a execução corrente;
2. Permite a verificação de todo o fluxo de processamento (O que também ajuda na escrita do relatório / artigo);
3. Diminuição do overhead de execução do trabalho.

Há alguns anos atrás, essa característica, era limitada nas pesquisas, por conta do uso de *software* com interfaces gráficas que acabam não permitindo a automação do trabalho realizado através dos "botões e clicks" na tela.

Hoje em dia, com o aumento e disseminação de linguagens de alto nível para o desenvolvimento de pesquisas, como [R](https://www.r-project.org/) e [Python](https://www.python.org/), isso mudou por completo. Podemos automatizar as tarefas de forma mais fácil. Além disso, a partir do momento que um script de processamento é criado, toda a lógica realmente aplicada nos dados é descrita de forma clara e direta.

Neste RC, para que todos as etapas pudessem ser modeladas através de *scripts*, fez-se a criação de diversas bibliotecas de código Python. Cada biblioteca possui uma responsabilidade única, o que nos ajudou a manter o trabalho organizado durante seu desenvolvimento. Ao mesmo tempo, essa abordagem facilita a reutilização dos códigos criados. Aqueles que desejam reutilizar o trabalho desenvolvido, podem fazê-lo com a importação dessas bibliotecas em seu projeto Python.

## Bibliotecas de código disponíveis

Para a adoção dessa abordagem de desenvolvimento, baseada em bibliotecas de responsabilidade única, que pudessem ser reutilizadas, fez-se necessário a adoção de alguns critérios que nos ajudasse a manter tudo organizado e reutilizável. Além disso, nossa visão com a criação de várias bibliotecas para a composição dos *scripts* de processamento do trabalho é que essas, devem ser modeladas de modo a possibilitar seu uso conjunto. Como blocos que podem ser juntados para construir um muro. 

Considerando essas características, inicialmente foi definido que neste RC, dois tipos de bibliotecas seriam desenvolvidas:

`Base`

:   Bibliotecas que fornecem os recursos e funcionalidades base para a realização de  uma ação
    (e.g., Geração de bandas de ângulos)

`Aplicação`

:   Bibliotecas que através da união de bibliotecas **Base**, disponibiliza funcionalidades que 
    permitem a aplicação de diferentes metodologias e fluxos de processamento (e.g., Geração de 
    produtos harmonizados).

Partindo dessas definições, para a produção deste RC e a geração de seus resultados, fez-se o desenvolvimento de duas bibliotecas **Base**:

[s2-angs](https://github.com/marujore/s2-angs)

:   Disponibiliza funcionalidades para a geração de bandas ângulos de imagens Sentinel-2;


[sensor-harm](https://github.com/marujore/sensor-harm)

:   Permite a geração de produtos harmonizados.

<!-- Rever esse parágrafo -->
Essas bibliotecas estão disponíveis e podem ser instaladas como qualquer outra biblioteca da linguagem Python e utilizada em diferentes projetos. Assim, caso seja de seu interesse, é possível, por exemplo, instalar a biblioteca `sensor-harm` em seu projeto Python e utilizar as funcionalidades disponibilizadas para a geração de produtos harmonizados. Para ambas as bibliotecas a única restrição está no respeito aos formatos de entradas esperados pelas funções dessas bibliotecas. Ao seguir corretamente, você não deverá ter problemas para fazer sua utilização.

<!-- Rever esse parágrafo: Deixar claro a relação "Com base" -->
Com base nessas duas bibliotecas, fez-se a criação de uma biblioteca **Aplicação**:

[research-processing](#)

:   Fornece funcionalidades que permitem a aplicação da metodologia de processamento de dados utilizadas na geração dos resultados deste RC. Parte de suas funcionalidades é criada com base nas bibliotecas `s2-angs` e `sensor-harm`.

Para resumir, a relação entre essas bibliotecas é sumarizada na Figura abaixo.

<figure markdown>
  ![Libraries organization](/assets/tools/libraries/libraries-organization/libraries-organization.svg){ width="1024" }
  <figcaption>Libraries organization</figcaption>
</figure>

Detalhes do funcionamento e funcionalidades de cada uma dessas bibliotecas são apresentados nas seções a seguir.

## Bibliotecas na metodologia dos experimentos

Para que se tenha uma ideia onde cada uma das bibliotecas apresentadas anteriormente são utilizadas na metodologia de processamento realizada neste RC, tem-se na Figura abaixo a relação de cada uma das etapas e a biblioteca utilizada.

<figure markdown>
  ![Processing workflow with libraries](/assets/tools/libraries/experiment-diagram/experiment-diagram.svg){ width="1024" }
  <figcaption>Processing workflow with libraries</figcaption>
</figure>

## Especificação das bibliotecas

Nesta seção, de forma complementar a visão geral apresentada até aqui, é feita a especificação das `funcionalidades` e `forma de uso` de cada uma das bibliotecas mencionadas anteriormente. 

### Sentinel-2 Angle Generator Python Library (s2-angs)
[![s2-angs-badge-stars](https://img.shields.io/github/stars/marujore/s2-angs?style=social)](https://github.com/marujore/s2-angs)
[![s2-angs-badge-forks](https://img.shields.io/github/forks/marujore/s2-angs?style=social)](https://github.com/marujore/s2-angs)
[![s2-angs-badge-version](https://img.shields.io/github/v/release/marujore/s2-angs?style=social)](https://github.com/marujore/s2-angs)

A biblioteca [s2-angs](https://github.com/marujore/s2-angs), como mencionado anteriormente, é responsável pela geração de bandas de ângulos para imagens Sentinel-2. Essas bandas contém informações, por pixel, de ângulos solar azimutal (SAA), solar zenital (SZA), sensor azimutal (VAA) e sensor zenital (VZA). Essas informações são extraídas dos metadados de imagens Sentinel-2. Inicialmente esses dados são fornecidos em forma de matrizes de `23x23` (linhas X colunas), ou seja, em uma resolução espacial de aproximadamente `5000` metros. Entretanto, essa informação precisa estar em resolução espacial equivalente à das bandas espectrais do sensor (`10`, `20` ou `60` metros) para que possam ser aproveitadas em correções por pixel. Assim, a biblioteca s2-angs é capaz de estimar os ângulos e salvá-slos arquivos `.tif`, tanto em sua resolução espacial original, quanto reamostrados para a resolução espacial das bandas do sensor.

Com isso, pode-se listar como funcionalidades principais dessa biblioteca:

- Geração de bandas de ângulos ( `SAA`, `SZA`, `VAA` e `VZA` );
- Reamostragem das bandas de ângulos para resolução de bandas do próprio sensor.

#### Principais operações disponíveis

A tabela abaixo apresenta um resumo das principais operações que estão disponíveis na biblioteca [s2-angs](https://github.com/marujore/s2-angs).

<div align="center" markdown>
|     **Function**      |                 **Description**                 |
|:---------------------:|:-----------------------------------------------:|
| `s2_angs.gen_s2_ang`  | Function to generate the Sentinel-2 Angle bands |
</div>

#### Exemplo de utilização

Para realizar a geração de banda de ângulo utilizando a biblioteca `s2_angs`, basta fazer o uso da função `gen_s2_ang`. Essa função aceita como entrada `.zip`, `.SAFE directory` ou `diretório com imagens Sentinel-2`. No bloco de código abaixo, tem-se um exemplo em que um arquivo `.zip` é utilizado como entrada na função:

```py linenums="1" title="s2-angs example code"
import s2_angs

s2_angs.gen_s2_ang(
  "S2B_MSIL1C_20191223T131239_N0208_R138_T23KMR_20191223T135458.zip"
)
```

O código acima fará a geração das bandas de ângulos da imagem definida na entrada. Exemplos de resultados podem ser visualizados nas figuras abaixo:

**Intermediary results (matrix 23x23)**

=== "Solar Azimuth"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/Solar_azimuth_23.png){ width=320" }
      <figcaption>Solar Azimuth intermediary result</figcaption>
    </figure>


=== "Solar Zenith"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/Solar_zenith_23.png){ width=320" }
      <figcaption>Solar Zenith intermediary result</figcaption>
    </figure>


=== "View Azimuth"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/View_azimuth_23.png){ width=320" }
      <figcaption>View Azimuth intermediary result</figcaption>
    </figure>

=== "View Zenith"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/View_zenith_23.png){ width=320" }
      <figcaption>View Zenith intermediary result</figcaption>
    </figure>

**Resampled results**

=== "Solar Azimuth"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/Solar_azimuth_resampled.png){ width=320" }
      <figcaption>Solar Azimuth resampled result</figcaption>
    </figure>

=== "Solar Zenith"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/Solar_zenith_resampled.png){ width=320" }
      <figcaption>Solar Zenith resampled result</figcaption>
    </figure>

=== "View Azimuth"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/View_azimuth_resampled.png){ width=320" }
      <figcaption>View Azimuth resampled result</figcaption>
    </figure>

=== "View Zenith"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/s2-angs/code-example-results/View_zenith_resampled.png){ width=320" }
      <figcaption>View Zenith resampled result</figcaption>
    </figure>

Para mais informações, por favor, consulte o [repositório oficial da biblioteca s2-angs](https://github.com/marujore/s2-angs).

## Sensor Harmonization Python Library (sensor-harm)
[![s2-angs-badge-stars](https://img.shields.io/github/stars/marujore/sensor-harm?style=social)](https://github.com/marujore/sensor-harm)
[![sensor-harm-badge-forks](https://img.shields.io/github/forks/marujore/sensor-harm?style=social)](https://github.com/marujore/sensor-harm)
[![sensor-harm-badge-version](https://img.shields.io/github/v/release/marujore/sensor-harm?style=social)](https://github.com/marujore/sensor-harm)

Neste RC, parte dos resultados consiste em produtos harmonizados, ou seja, produtos de nível de reflectância de superfície com correção para os efeitos de `Função de distribuição de reflectância bidirecional` (BRDF) e ajustes espectrais. Para isso, fez-se a criação da biblioteca [sensor-harm](https://github.com/brazil-data-center/sensor-harm). Nessa biblioteca, a correção BRDF é feita utilizando o método do `c-factor` para gerar produtos Nadir BRDF-Adjusted Reflectance (NBAR), enquanto que o ajuste espectral é feito utilizando `bandpass` adotando as imagens Landsat-8 como referência. Com o uso dessa biblioteca, esses métodos podem ser aplicados em imagens dos satélites-sensores Landsat-4/TM, Landsat-5/TM, Landsat-7/ETM+, Landsat-8/OLI e Sentinel-2/MSI, além de permitir a harmonização entre esses diferentes dados. A biblioteca apresenta duas funções principais, uma para harmonizar imagens provenientes de sensores a bordo dos satélites Landsat e outra para imagens provenientes dos sensores a bordo dos satélites Sentinel-2.

#### Principais operações disponíveis

A tabela abaixo apresenta um resumo das principais operações que estão disponíveis na biblioteca [sensor-harm](https://github.com/brazil-data-center/sensor-harm).

<div align="center" markdown>
|     **Function**                           |                 **Description**                 |
|:------------------------------------------:|:-----------------------------------------------:|
| `sensor_harm.landsat.landsat_harmonize`    |       Function to harmonize Landsat data        |
| `sensor_harm.sentinel2.sentinel_harmonize` |       Function to harmonize Sentinel-2 data     |
</div>

#### Exemplo de utilização

Para realizar a harmonização de dados, seja esse Landsat-4/TM, Landsat-5/TM, Landsat-7/ETM+, Landsat-8/OLI ou Sentinel-2, é necessário definir o diretório onde os dados de entrada estão armazenados, bem como o diretório de saída. Para exemplificar o uso dessa função, o bloco de código abaixo é um exemplo de como a biblioteca `sensor-harm` pode ser utilizada para harmonização de dados Sentinel-2:

```py linenums="1" title="sensor-harm example code"
from sensor_harm.sentinel2 import sentinel_harmonize

sentinel2_entry = '/path/to/S2/SR/images/'
target_dir = '/path/to/output/NBAR/'

sentinel_harmonize(sentinel2_entry, target_dir, apply_bandpass=True)
```

O código acima fará a geração das bandas de ângulos da imagem definida na entrada. Exemplos de resultados podem ser visualizados nas figuras abaixo:

**Sentinel-2/MSI Harmonized Data**

=== "NBAR Band 02 (10m)"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/sensor-harm/code-example-results/T22KGA_20210713T132241_B02_10m_NBAR.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image (B02) NBAR 10m</figcaption>
    </figure>

=== "NBAR Band 03 (10m)"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/sensor-harm/code-example-results/T22KGA_20210713T132241_B03_10m_NBAR.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image (B03) NBAR 10m</figcaption>
    </figure>


=== "NBAR Band 04 (10m)"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/sensor-harm/code-example-results/T22KGA_20210713T132241_B04_10m_NBAR.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image (B04) NBAR 10m</figcaption>
    </figure>

=== "NBAR Band 08 (10m)"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/sensor-harm/code-example-results/T22KGA_20210713T132241_B08_10m_NBAR.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image (B08) NBAR 10m</figcaption>
    </figure>

=== "NBAR Band 08A (20m)"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/sensor-harm/code-example-results/T22KGA_20210713T132241_B8A_20m_NBAR.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image (B8A) NBAR 20m</figcaption>
    </figure>

=== "NBAR Band 11 (20m)"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/sensor-harm/code-example-results/T22KGA_20210713T132241_B11_20m_NBAR.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image (B11) NBAR 20m</figcaption>
    </figure>

=== "NBAR Band 12 (20m)"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/sensor-harm/code-example-results/T22KGA_20210713T132241_B12_20m_NBAR.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image (B12) NBAR 20m</figcaption>
    </figure>

Para mais informações, por favor, consulte o [repositório oficial da biblioteca sensor-harm](https://github.com/marujore/sensor-harm).

## Research Processing Python Library (research-processing)

A metodologia de processamento realizada neste RC, conforme apresentado nas seções anteriores, possui diversas etapas, as quais dependem de diferentes ferramentas de software. Consequentemente, a realização de todo o fluxo de processamento pode exigir:

1. Instalação de dependências de software específicas para cada etapa de processamento;
2. Configurações específicas no ambiente de software para cada etapa de processamento.

Com essas exigências, a execução e reprodução do fluxo de processamento poderiam ser problemáticas para nós e para aqueles que desejassem reproduzir ou mesmo aplicar o trabalho desenvolvido. Como forma de evitar esses possíveis problemas e facilitar a materialização da metodologia de processamento deste RC, nós desenvolvemos a biblioteca `research-processing`. Nessa biblioteca, todas as etapas da metodologia são modeladas como funções Python que podem ser facilmente utilizadas na construção de qualquer fluxo de processamento. Adicionalmente, parte das operações que exigem configurações específicas de ambiente, são executadas em `Docker Containers`, de forma transparente aos usuários da biblioteca. Ao todo, tem-se no `research-processing`, funcionalidades para a realização de ações como:

**Pré-processamento**

- Correção atmosférica Sentinel-2/MSI (Sen2Cor e LaSRC);
- Geração de bandas de ângulos (Landsat-8/OLI e Sentinel-2/MSI);
- Geração de produtos NBAR (Sentinel-2/MSI e Landsat-8/OLI).

**Análise de dados**

- Rotinas de validação das correções realizadas.

### Abordagem de execução das funções

Assim como mencionado anteriormente, as funcionalidades do `research-processing` são modeladas como funções reutilizáveis com execução amigável a reprodução. Para que essas características pudessem ser garantidas, adotou-se na biblioteca durante a implementação das funções, o conceito de `modelo de execução`, o qual determina onde/como a função será executada, de forma transparente ao usuário. Cada uma das funções implementadas na biblioteca possui um `modelo de execução`, permitindo que diferentes tecnologias e abordagens sejam utilizadas como base para a execução da função. Partindo das necessidades das funções desse RC, fez-se o uso de dois `modelos de execução` nas implementações realizadas, sendo eles:

`Local`

:   Funções implementadas com o modelo de execução `Local`, são funções Python simples. Essas funções não possuem nenhum formato de execução especial, sendo executados diretamente no ambiente/interpretador que a invocou. Funções com esse formato, dependem do ambiente adjacente, sendo necessário para esse, ter todas as dependências instaladas e devidamente configuradas.

`Containerized`

:   Diferente de funções `Local`, as funções `Containerized` não dependem do ambiente adjacente. Isso porque funções implementadas com esse formato, ao serem executadas, criam um `Docker Container`, com o ambiente completo necessário para a execução da operação associada a função. A função é executada dentro do ambiente criado.

Ambos modelos de execução, são transparentes para o usuários no momento da execução. Assim, independente da forma com que a implementação foi realizada, o uso final é o mesmo: Uma chamada a uma função Python. A diferença está nas exigências que cada tipo de função fará do ambiente onde está sendo executada. Para as funções `Local`, como mencionado, será necessário a instalação de todas as dependências e configurações para que a função seja executada. Enquanto isso, as funções `Containerized` exigirão a disponibilidade do Docker no ambiente do usuário.

!!! info "Containerized - Permissões de usuário"

    É importante notar que, além do Docker instalado, é necessário também que o usuário que está fazendo a execução, tenha as devidas permissões para utilizar o Docker. 

Na Figura abaixo, faz-se uma representação geral de cada um desses modelos utilizados. Note que, funções `Local`, trabalham com o interpretador Python, enquanto funções `Containerized` criam `Docker Containers` onde a execução será realizada.

<figure markdown>
  ![Libraries organization](/assets/tools/libraries/research-processing/execution-model/execution-model-example.svg){ width="1024" }
  <figcaption>Research Processing Execution Models</figcaption>
</figure>

Com base nesses dois modos de operação, a biblioteca implementa e disponibiliza as operações de `processamento` e `análise` dos dados. Para as operações de processamento, que utilizam ferramentas terceiras, como **Sen2Cor** e **LaSRC**, faz-se o uso do modo de operação `Containerized`. Já nas operações de validação, que dependem apenas de bibliotecas Python, usa-se o modo de operação `Local`.

#### Comunicação entre as funções

As funcionalidades da biblioteca `research-processing` podem ser utilizadas em conjunto, de modo a construir um fluxo de processamento que permita a materialização da metodologia de experimento seguida nesse RC. Nesse contexto, um ponto a ser considerado sobre o funcionamento da biblioteca é a forma com que as entradas e saídas dessas funções podem ser encadeadas, de modo que a saída de uma função é utilizada como entrada em outra função.

No `research-processing`, as operações implementadas são realizadas de modo a evitar a movimentação de dado (Entradas e saídas). Para isso, as funções de processamento operam com base no `caminho de dados`. Com isso, as funções recebem o caminho onde os dados estão armazenados, bem como onde os resultados devem ser salvos. Tal modo de operação permite melhores definições em relação ao local onde os dados serão carregados e salvos, evitando movimentações desnecessárias e armazenamento em locais que podem apresentar problemas com o limite de espaço e baixo desempenho. Esse modo de funcionamento é representado na figura abaixo.

<figure markdown>
  ![Libraries organization](/assets/tools/libraries/research-processing/data-flow/data-flow.svg){ width="1024" }
  <figcaption>Modelo de comunicação entre funções</figcaption>
</figure>

Com base nesse modo de funcionamento, as funções são encadeadas e as saídas de uma função, que representam o caminho para onde os dados foram salvos, são utilizados como entrada em outras funções.

!!! info "Entradas como volumes"

    Deve-se notar que essas informações de caminho de dados, para as funções `Containerized`, são utilizadas para a criação de [Docker Bind Mount Volumes](https://docs.docker.com/storage/volumes/). Assim, os Containers auxiliares tem acesso aos dados que devem ser processados.

!!! caution "Ordem de execução das operações"

    Com esse formato de entradas/saídas das funções, tem-se como premissa que a saída de uma função será entendida pela função seguinte. Sendo assim, as funções disponíveis na biblioteca `research-processing`, devem ser encadeadas em uma ordem estrita, sendo nesse caso, a ordem descrita na metodologia.

    Para mais detalhes de como isso pode ser implementado, consulte a seção [Scripts de processamento](/pt/tools/processing/).


### Principais operações disponíveis

Para dar suporte a criação de todo o fluxo de operação implementado nesse RC, a biblioteca `research-processing` fornece diversas funções e operações auxiliares, as quais são listadas na tabela abaixo:


|                      **Função**                      |                                         **Descrição**                                         | **Modelo de execução** |
|:----------------------------------------------------:|:---------------------------------------------------------------------------------------------:|:----------------------:|
|   `research_processing.surface_reflectance.sen2cor`  |                        Correção Atmosférica Sen2Cor para Sentinel-2/MSI                       |      Containerized     |
|    `research_processing.surface_reflectance.lasrc`   |                         Correção atmosférica LaSRC para Sentinel-2/MSI                        |      Containerized     |
|      `research_processing.nbar.s2_sen2cor_nbar`      | Gerador de produtos NBAR para dados Sentinel-2/MSI  Reflectância de superfície com (Sen2Cor). |      Containerized     |
|       `research_processing.nbar.s2_lasrc_nbar`       |   Gerador de produtos NBAR para dados Sentinel-2/MSI Reflectância de superfície com (LaSRC).  |      Containerized     |
|          `research_processing.nbar.lc8_nbar`         |         Gerador de produtos NBAR para dados Landsat-8/OLI  Reflectância de superfície.        |      Containerized     |
|    `research_processing.nbar.lc8_generate_angles`    |                          Gerador de ângulos para dados Landsat-8/OLI                          |      Containerized     |
| `research_processing.validation.validation_routines` |                     Análise de resultados  (Módulo com múltiplas funções)                     |          Local         |

Dentre essas funções, há alguns detalhes que precisam ser considerados para o entendimento completo do motivo por trás de cada um dos `modelos de execução` escolhidos para as funções. Nos subtópicos abaixo, esses detalhes são apresentados:

**Correção atmosférica Sentinel-2/MSI (Sen2Cor e LaSRC)**

O fluxo de processamento exige que as imagens utilizadas tenham correção atmosférica. Para as imagens Landsat-8/OLI, não há a necessidade de fazer a correção, uma vez que os produtos já são disponibilizados prontos para uso, com as devidas correções geométricas e radiométricas realizadas. No entanto, para os dados Sentinel-2/MSI, isso não é verdade. Assim, durante o desenvolvimento do artigo foi necessário realizar a correção atmosférica desses dados. Para isso, adotou-se as ferramentas [Sen2Cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/) e [LaSRC](https://ntrs.nasa.gov/api/citations/20190001670/downloads/20190001670.pdf).

Essas ferramentas possuem suas necessidades específicas no ambiente onde serão utilizadas, como dependências e configurações para seu uso. Considerando isso, na biblioteca `research-processing` fez-se a criação de funções que operam essas ferramentas em um ambiente já configurado e pronto para uso. Esse ambiente é executado em um `Docker Container`.

Das funções apresentadas na tabela acima, as listadas a seguir são utilizadas para aplicar a correção atmosférica nos dados:

- `research_processing.surface_reflectance.lasrc`: Função que faz a aplicação de Correção Atmosférica em dados Sentinel-2/MSI utilizando a ferramenta LaSRC. Todo o processamento é realizado dentro de um `Docker Container` de forma transparente para o usuário;
- `research_processing.surface_reflectance.sen2cor`: Função que faz a aplicação de Correção Atmosférica em dados Sentinel-2/MSI utilizando a ferramenta Sen2Cor. Todo o processamento é realizado dentro de um `Docker Container` de forma transparente para o usuário.

!!! info "Entendendo os Containers"

    A criação de um `Docker Container` depende de uma `Docker Image` que define o ambiente e suas configurações. Isso não é diferente no `research-processing`. Para a criação dos `Docker Containers` de Correção Atmosférica, são utilizadas as seguintes `Docker Images`:

      - Correção atmosférica com LaSRC: [Docker Image LaSRC 2.0.1](/pt/tools/environment/#lasrc-201)
      - Correção atmosféria com Sen2COr: [Docker Image Sen2Cor 2.9.0](/pt/tools/environment/#sen2cor-290)
    
    Essas `Docker Images` foram criadas para execução nesse RC. Para mais informações, consulte a seção [Ambientes computacionais](/pt/tools/environment).

**Geração de bandas de ângulos (Landsat-8/OLI e Sentinel-2/MSI)**

Para a geração dos produtos NBAR, faz-se necessário que bandas de ângulos (e.g., SAA, SZA, VAA and VZA) sejam calculadas. Essas bandas são geradas de forma específica para cada dados/sensor que está sendo trabalhada. Com isso, faz-se necessário o uso de ferramentas especializadas para cada sensor:

- Landsat-8/OLI: A geração de bandas de ângulos para o Landsat-8/OLI é feita através da ferramenta [Landsat 8 Angles Creation Tools](https://www.usgs.gov/media/files/landsat-8-angles-creation-tools-readme). Essa ferramenta possui suas próprias dependências, exigindo também configurações específicas no ambiente onde será executada;
- Sentinel-2/MSI: Os ângulos de dados Sentinel-2/MSI são gerados com a biblioteca [Sentinel-2 Angle Generator Python Library (s2-angs)](/pt/tools/libraries/#sentinel-2-angle-generator-python-library-s2-angs), desenvolvida nesse RC.

Considerando essas características, tem-se a seguinte função para executar essas operações:

- `research_processing.nbar.lc8_generate_angles`: Função que através da ferramenta [Landsat 8 Angles Creation Tools](https://www.usgs.gov/media/files/landsat-8-angles-creation-tools-readme), realiza o cálculo das bandas de ângulos para dados Landsat-8/OLI. O processamento realizado por essa função é feito dentro de um `Docker Container`.

Na lista de funções acima, não há nenhuma função específica para o Sentinel-2/MSI. Isso ocorre já que, durante a implementação da biblioteca `research-processing`, foi decidido que a geração de ângulos para os dados Sentinel-2/MSI seria uma operação integrada a geração dos produtos NBAR. Assim, o cálculo dos ângulos necessários para a geração dos produtos NBAR com dados Sentinel-2/MSI, feitos com a biblioteca s2-angs, são parte das seguintes funções:

  - `research_processing.nbar.s2_sen2cor_nbar`
  - `research_processing.nbar.s2_lasrc_nbar`

O processamento realizado por ambas as funções listadas acima também é feito dentro de um `Docker Container`.

!!! info "Entendendo os Containers"

    A criação de um `Docker Container` depende de uma `Docker Image` que define o ambiente e suas configurações. Isso não é diferente no `research-processing`. Para a criação do `Docker Container` de geração de banda de ângulos, é feito o uso da seguinte `Docker Image`:

      - Geração de bandas de ângulos para dados Landsat-8/OLI: [Docker Image L8Angs](/pt/tools/environment/#l8angs)
    
    Essas imagens foram criadas para execução nesse RC. Para mais informações, consulte a seção [Ambientes computacionais](/pt/tools/environment).

**Geração de produtos NBAR (Sentinel-2/MSI e Landsat-8/OLI)**

A base para a geração dos produtos NBAR nesse RC, conforme apresentado nas seções anteriores, é a biblioteca `sensor-harm`. Essa biblioteca, permite a geração de produtos NBAR para dados Sentinel-2/MSI e Landsat-8/OLI. Como forma de facilitar a utilização da biblioteca `sensor-harm` e evitar que os utilizadores tenham de fazer instalações e configurações específicas, na biblioteca `research-processing` foi realizada a implementação das seguintes funções:

- `research_processing.nbar.lc8_nbar`: Faz a geração de produtos NBAR para dados Landsat-8/OLI
- `research_processing.nbar.s2_lasrc_nbar`: Faz a geração de produtos NBAR para dados Sentinel-2/MSI com correção atmosférica feita com a ferramenta LaSRC;
- `research_processing.nbar.s2_sen2cor_nbar`: Faz a geração de produtos NBAR para dados Sentinel-2/MSI com correção atmosférica feita com a ferramenta Sen2Cor.

Essas funções, são implementadas com o `modelo de execução` Containerized. Assim, no momento em que o usuário faz a execução dessas funções, um `Docker Container`, com as devidas dependências é criado para executar a função.

!!! info "Entendendo os Containers"

    A criação de um `Docker Container` depende de uma `Docker Image` que define o ambiente e suas configurações. Isso não é diferente no `research-processing`. Para a criação do `Docker Container` de geração de produtos NBAR (todas as funções), é feito o uso da seguinte `Docker Image`:

      - Geração de produtos NBAR (Sentinel-2/MSI e Landsat-8/OLI): [Docker Image NBAR](/pt/tools/environment/#nbar)
    
    Essas imagens foram criadas para execução nesse RC. Para mais informações, consulte a seção [Ambientes computacionais](/pt/tools/environment).

**Rotinas de validação das correções realizadas**

Para finalizar as funcionalidades, tem-se o módulo de validação de correções. Esse módulo (`research_processing.validation.validation_routines`), é o responsável em fazer todas as comparações e cálculos utilizados para avaliar os resultados gerados neste RC. De modo a tornar a depuração mais simples e direta, sua implementação é feita com o `modelo de execução` Local. Com isso, o usuário que utilizar as funções desse módulo, deve configurar o ambiente onde a execução será feita. Em resumo, tem-se apenas que instalar as dependências da própria biblioteca `research-processing` e então o ambiente já estará pronto para executar essas funções.

### Exemplo de utilização

Para exemplificar a forma de utilização da biblioteca `research-processing`, abaixo é apresentada a forma com que a biblioteca realiza a correção atmosférica de imagens Sentinel-2/MSI, utilizando a ferramenta [Sen2Cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/).

**Correção atmosférica Sen2Cor**

```py linenums="1" title="Sen2Cor atmosphere correction example with research-processign library"
from research_processing.surface_reflectance import sen2cor

# sen2cor(
#  input_dir  = "<path to directory where .safe is>", 
#  output_dir = "<path where result will be saved>" , 
#  scene_ids  = ["<scene ids of `input_dir` that will be processed>"]
#)
# For example:
sen2cor(
  input_dir  = "/data/input", 
  output_dir = "/data/output" , 
  scene_ids  = ["S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE"]
)
```

O código acima fará a geração de imagens com correção atmosférica. Exemplos de resultados podem ser visualizados nas figuras abaixo:

**Atmospheric Corrected Images with Sen2Cor**

=== "10m resolution"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/research-processing/code-example-results/T22KGA_20210723T132241_TCI_10m.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image with Atmospheric Correction (10m resolution)</figcaption>
    </figure>


=== "20m resolution"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/research-processing/code-example-results/T22KGA_20210723T132241_TCI_20m.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image with Atmospheric Correction (20m resolution)</figcaption>
    </figure>


=== "60m resolution"

    <figure markdown>
      ![Processing workflow with libraries](/assets/tools/libraries/research-processing/code-example-results/T22KGA_20210723T132241_TCI_60m.png){ width=512" }
      <figcaption>Sentinel-2/MSI Image with Atmospheric Correction (60m resolution)</figcaption>
    </figure>
