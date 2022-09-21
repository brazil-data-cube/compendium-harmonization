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

# Auxiliary scripts

Besides the codes, in this RC that, that generates the results, a few auxiliary *scripts* were also developed. In this section, these *scripts* are detailed.

### Calculate Checksum and GitHub Asset Upload

To share this RC, all its materials were made available through a GitHub repository, which contains all the historic of modification on materials, code, documentation and data.

The *scripts* and documentation does not uses much disk volume, so it could be stored directly in GitHub. However, auxiliary data, that are used in minimal example and replication are larger and cannot be stored in a common repository. As an alternative, these files were published through the [Release Assets](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), which supports files of up to 2 GB to be stored and maintained in the repository.

To prepare and organize the data as GitHub Release Assets two auxiliary *scripts* were made:

`Calculate Checksum`

:   `Calculate Checksum` is a Python *script* that creates a [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) and stores their files as `zip`.

`GitHub Asset Upload`

:   Once the [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) are created, the R *script* `GitHub Asset Upload` uploads them to the GitHub servers, which is done with the package [piggyback](https://github.com/ropensci/piggyback).

Using these two scripts the data was made available on the same repository that contains the processing scripts and documentation.

### Example toolkit

Considering that since the data is on Github and that anyone can obtain the, to execute the examples of this RC, it is necessary that the data is organized in [the RC correct directories](/en/#research-compendium-organization).

To solve this and avoid manual *download* and organization, we provide a Python *script*, the `Example toolkit`, that automatically perform these steps. The only configuration a user must do is to define a directory for the *download*.

#### Operation

The `Example toolkit` *script* will execute four main steps, as illustrated on the Figure bellow:

<figure markdown>
  ![libs-link](/assets/tools/utilitary/example-toolkit/operation-flow.svg){ width="1024" }
  <figcaption>Example Toolkit Operation Flux</figcaption>
</figure>

The `Example toolkit` *sript* performs the data *download* (from the [GitHub Release Assets](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)). Following, it verifies if the downloaded data haven't suffered any changes or if they are corrupted. This is performed using the downloaded BagIts. Then, the tool *scrit* extract the data to the correct folders. Finally, using the users definitions and directives of where the data was downloaded, it generates a [Dagster configuration file](/en/tools/processing/#arquivo-de-configuracao-dagster), which can be used to start the processing of the downloaded data.


!!! info "Dagster and configuration files"

    If you are interested in learning more on how Dagster is used in this RC and where the configuration file should be used, consult the Section [Processing Scripts - Dagster](/en/tools/processing/#dagster-configuration-file).


#### Use

<!-- ToDo: Atualizar o link do diretório toolkit no github -->

To use the `Example toolkit` *script*, only Python is required with the environment requisites.

!!! tip "Example toolkit with Docker"

    To use the`Example toolkit` with no environment configuration, consult the section [Example toolkit environment](/en/tools/environment/#example-toolkit-environment) for more information on how you can use the Docker version of the script.

!!! tip "Manual configuration of the environment"

    To manually configure the Python environment and the dependencies required to run the `Example toolkit`, you can use [conda](https://docs.conda.io/en/latest/). With this package manager, you can create a new environment with the `Example toolkit` requirements. To create this environment, use the file `environment.yml` that can be found in the directory [tools/example-toolkit](#):

    ``` shell
    conda env create -f environment.yml
    ```

To execute the `Example toolkit` you must define its configurations, which will be used to deremine the local to write the data and some parameters to auxiliate the *script* generates the Dagster configuration file. This configuration is done through environment variables, being them:

<!-- ToDo: Atualizar o link do Exemplo mínimo e replicação para o github -->

`DOWNLOAD_REFERENCE_FILE`

:   Environment variable to determine the absolute path of the `JSON` which defines where the GitHub Assets Release data will be downloaded. Examples of this file can be found in the directory [tools/example-toolkit/config](#).
:   *Value example*: `/compendium/config/example-toolkit.json`

`DOWNLOAD_OUTPUT_DIRECTORY`

:   Environment variable that determines the directory where the downloaded data will be stored. The data is organized following the format of the [Data directory](/en/tools/processing/#diretorio-de-dados), required by the processing *scripts*.
:   *Value example*: `/compendium/data`

`PIPELINE_DIR` (Dagster Configuration)

:   Environment variable that determines where the Dagster Configuration file will be saved.
:   *Value example*: `/compendium/config/config.yml`

`RAW_DATA_DIR` (Dagster Configuration)

:   Environment variable that determines which directory should be considered as the machine [input dir](#) for the Dagster processing.
:   *Value example*: `/compendium/data/raw_data`

`DERIVED_DATA_DIR` (Dagster Configuration)

:   Environment variable that determines which directory should be considered as the machine [output dir](#) in the Dagster configuration file.
:   *Value example*: `/compendium/data/derived_data`

!!! note "Variable definition consistency"

    The configuration variables have a logical dependency that must be followed to avoid problems. To present this dependency let's consider the following example:

    Suppose that you wish to *download* the data on a directory `/opt/my-data`. In this case, you will define the `DOWNLOAD_OUTPUT_DIRECTORY` as:

    ``` sh
    DOWNLOAD_OUTPUT_DIRECTORY=/opt/my-data
    ```

    Knowing that your data will be organized following the pattern in [Data directory](/en/tools/processing/#diretorio-de-dados), the downloaded data will be stored as follows:

    ```
    /opt/my-data
        ├── derived_data
        └── raw_data
    ```

    Considering this organization, if you desire to generate the Dagster file to process data in `/opt/my-data`, it will be required to define the Dagster environment variables as:

    ``` sh
    # 1. Input dir
    RAW_DATA_DIR=/opt/my-data/raw_data

    # 2. Output dir
    DERIVED_DATA_DIR=/opt/my-data/derived_data
    ```

After defining each environment variable, the `Example toolkit` can be executed. To do that, the *script* available on the diretory [tools/example-toolkit/scripts/pipeline.py](#) must be executed. Considering that you are in the root of this RC, the execution of this *script* can be performed by:

*1. Changing directory*

``` sh
cd tools/example-toolkit/
```

*2. Execution*

``` sh
python3 scripts/pipeline.py
```

At the end of the execution, the output directories will appear as:

**Data**

The directory defined by the variable `DOWNLOAD_OUTPUT_DIRECTORY`, as mentioned, will follow the [Data directory](/pt/tools/processing/#diretorio-de-dados) organization, required by this RC processing scripts *scripts*. The data will be organized as:

```
DOWNLOAD_OUTPUT_DIRECTORY
    ├── derived_data
    └── raw_data
        ├── landsat8_data
        ├── sentinel2_data
        ├── scene_id_list
        └── lasrc_auxiliary_data
```

**Dagster Configuration**

The directory defined by the variable `PIPELINE_DIR` will be populated as a [Dagster configuration File](/en/tools/processing/#arquivo-de-configuracao-dagster) named `config.yaml`. In this file, the following content will be available:

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

For a complete and functional example of the `Example toolkit`, consult the section [Reproducible research - minimal example](/en/reproducible-research/minimal-example/).
