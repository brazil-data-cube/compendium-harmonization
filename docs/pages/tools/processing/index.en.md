<!-- Abbreviations -->
*[RC]: Research Compendium

# Processing Scripts

To implement this RC methodology, a [set of software libraries](/en/tools/libraries) was created. Using these libraries and their functionality, we implemented the processing *scripts*. These *scripts* are the materialization of this RC methodology experiments.

These *scripts* were processed using two tools:

[Jupyter Notebook](https://jupyter.org/): Interactive computation environment, that allows the creation of computational notebooks containing code and documentation;

[Dagster](https://docs.dagster.io/0.12.15/getting-started): Platform for creating, managing and executing processing chains and data manipulation.

Both implementation use the same libraries and versions to process, ensuting reproductible and comparable results. These two options were implemented due to:

1. Present the capabilities of the use of this RC libraries;
2. Coverage of the scenaries of this RC methodology;
3. Double implementation, which allowed to compare the genarated results in distinct ways, from the same tools.

The connhection between these processing *scripts* and the [software libraries](/en/tools/libraries) developed in this RC, are presented in the following Figure:

<figure markdown>
  ![libs-link](/assets/tools/processing/processing-scripts-libs-overview.svg){ width="1024" }
  <figcaption>Relation between software libraries and processing <i>scripts</i>.</figcaption>
</figure>

## Jupyter Notebook

When exploring the implemented methodology, it is desired that the processing steps should be well documented and organized. In the implemented Jupyter Notebook, all steps are documented and described, allowing users to understand and explore what is being processed. In the following video a few parts of the notebook are presented.

<figure markdown>
  ![libs-link](/assets/tools/processing/jupyter/jupyter-notebook-overview.gif){ width="1024" }
  <figcaption>Jupyter Notebook processing example.</figcaption>
</figure>

### Configurations

To use this Jupyter Notebook only one configuration is required: define the environmental variable `DATA_DIRECTORY`. This variable determines the data directory that will be used by the notebook to load input data and write the gererated results.

!!! tip "About the data directory"

    Details regarding how the data, defined through the environmental variable `DATA_DIRECTORY`, mus be organized are presented in the section [Data directory](#data-directory).

## Dagster

!!! warning "About Dagster version"

    When this RC was being developed, the dagster official version was `0.12.15`. Nowadays the versions have changed, and so have the nomenclature and definitions used by the *software*. To keep the content consistent, the explanations used in this documentation follow the base version `0.12.15`.

!!! warning "Nomenclatures"

    In Dagster, all the processing flux is called a **Pipeline**. In this document, to keep the explanations consistent to the ones performed in the Jupyter Notebook, the pipelines are generically treated as processing *scripts*.

    You can consult the [official Dagster Documentation (v0.12.15)](https://docs.dagster.io/0.12.15/getting-started) where you can find a detailed explanation of [Pipelines](https://docs.dagster.io/0.12.15/concepts/solids-pipelines/pipelines).

Once with an implemented methodology and ready to use, its execution alongside its big data can require several controls and actions as:

1. Parallel execution;
2. Failure Control;
3. Reexecution.

Based on that, the processing *script* using [Dagster](https://docs.dagster.io/0.12.15/getting-started) was created. With this tool, all the orchestration can be performed. Besides that, when configured, several different execution ways can be performed, for instance distributed and parallel. Another Dagester advantage is also failure control and reexecution.

The processing *script* creation is performed through a Python Application Programming Interface (API), nonetheless, the manipulation and use of the *script* is performed through a *web* interface. This interface presents the options to execute the processing, manage it as well as consult the documentation of each step and the performed flux. The video bellow presents a this interface:

<figure markdown>
  ![libs-link](/assets/tools/processing/dagster/dagster-overview.gif){ width="1024" }
  <figcaption>Dagster interface example containing part of the processing flux.</figcaption>
</figure>

### Configurations

To execute the processing *script* created with Dagster, it is required to configure the tool. This configuration is performed through the definition of a few parameters in a `YAML` file, which specifies:

1. Where input data are stored;
2. Which will be the output directory;
3. Which images and spectral bands should be used;
4. Computational resources specification (e.g., number of available CPUs).

Once this file is created, it is inserted in the Dagster interface, where it is validated and used to create a new *script* execution.

!!! tip "About Dagster executions"

    To lear more on how Dagster version `0.12.15` creates its executions, please, consult the [tool official documentation](https://docs.dagster.io/0.12.15/concepts/configuration/config-schema#config-schema)

In order to configure your Dagster parameters and execute your own data, the following subsection presents the `YAML` file used by Dagster.

#### Dagster Configuration File

The Dagster configuration file, is used to define the resources that will be used during the processing *script* execution. This file, in the `YAML` format, is divided in two main sections: (i) Resources; (ii) Solids.

!!! tip "About the configuration file"

    When using the Jupyter Notebook, all configuration is performed through a unique environmental variable (`DATA_DIRECTORY`). In Dagster, the configuration file has the same role.

    Thus, it is recommended to consult the [Data directory](#data-directory) section before you configure the file. In the mentioned section the directory structure, that must be followed, is described, as well as the content that must be available in each section.

##### Resources

In Dagster, [resources](https://docs.dagster.io/0.12.15/concepts/modes-resources#overview) are used to represent elements and computational resourses that **must** be available for the processing *script* execution. The *resources* represent the data that must be used during the processing. Thus, a *resource*, can have one or more data directories. The processing *script* requires two *resources*:

**lasrc_data**

*Resource* containing data related to the LaSRC tool. The defition of a `lasrc_data` *resource* requires the specification of the following configuration variable:

`lasrc_auxiliary_data_dir`: Variable that defines the path to the directory containing the LaSRC auxiliary files, required to perform the atmospheric correction processing (used in this RC for Sentinel-2/MSI).


!!! info "Data directory organization"

    For more details on how these auxiliary data must be organized, please consult the section [Data directory](#data-directory).

A complete example of the `lasrc_data` *resource* definition is presented bellow:

```yaml
resources:
  lasrc_data:
    config:
      lasrc_auxiliary_data_dir: /path/to/lasrc/auxiliary/data
```

This block of code must be defined within the configuration file. For a complete example, please consult the [dagster configuration file](#full-example).

**repository**

*Resource* that defines the input and output of the processing *script*. The definition of a `repository` *resource* requires the specification of the following configuration variables:

`landsat8_input_dir`: Directory containing the Landsat-8/OLI data, that can be used as input for the processing *script*;

`sentinel2_input_dir`: Directory containing the Sentinel-2/MSI data, that can be used as input for the processing *script*;

`derived_data_dir`: Directory in which the output data will be written.

!!! info "Data Directory Organization"

    For more details on how each of these directories should be organized, please, consult the section [Data directory](#data-directory).

A complete example on the `repository` *resource*  definition is presented bellow:

```yaml
resources:
  repository:
    config:
      derived_data_dir: /path/to/derived/data/dir
      landsat8_input_dir: /path/to/input/landsat8/data/dir
      sentinel2_input_dir: /path/to/input/sentinel2/data/dir
```

This block of code must be defined within the configuration file. For a comple example, consult the [dagster configuration file](#full-example).

##### Solids

In Dagster, [solids](https://docs.dagster.io/0.12.15/concepts/solids-pipelines/solids#solids) represents the working unity that will execute the operation. These elements are responsible for receiving inputs, performing the processing and generate the output. Thus, the processing *script*, they were used to represent each of the processing steps.

The **solids** an require a configuration for their definition. In this RC processing *script* only one of them requires configuration:

`load_and_standardize_sceneids_input`: *solid* responsible for receiving the orbital scenes to be processed. The *solid* reads, validates and pass the loaded information for the following processing steps. During this *solid* configuration, it is required to specify the following configuration variables:

- `landsat8_sceneid_list`: `.txt` file containing the name of all Landsat-8/OLI scenes that will be considered during the processing flux. These names must be the same as the ones available in the Landsat-8/OLI data directory (`landsat8_input_dir`) specified in the `repository` *resource*;

- `sentinel2_sceneid_list`: `.txt` file containing the name of all Sentinel-2/MSI scenes that will be considered during the processing flux. These names must be the same as the ones available in the Sentinel-2/MSI data directory (`sentinel2_input_dir`) specified in the `repository` *resource*;

!!! info "Data directory organization"

    For more details on how the files containing the scene names should be organized, please consult the section [Data directory](#data-directory).

A complete definition of the `load_and_standardize_sceneids_input` *solid*  is presented bellow:

```yaml
solids:
  load_and_standardize_sceneids_input:
    config:
      landsat8_sceneid_list: /path/to/input/landsat8/data/landsat.txt
      sentinel2_sceneid_list: /path/to/input/sentinel2/data/sentinel.txt
```

##### Complete example

Bellow is presented a complete Dagster configuration file, that uses all *resources* and *solids* specified in the previous topics:

To exemplify all the cited elements in a configuration file, bellow is presented the minimal configuration required to execute this RC pipeline.

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

## Data directory

In both implementations of the processing *scripts*, in the configuration step, it is required to define the path to the input directory containing the data. This directory has a standard organization, that is used by any of the two processing approaches. In this section, the organization of the data directory will be presented. To start it is important first to understand that:

!!! quote ""

    The data directory, used in both processing *scripts* approaches, represent the input and output directories of the *script*. All the inputs are read from this directory only, not being able to read from a different directory. The same occurs for the output, the results produced are only stored in this directory.

The logic behind this definition is organization: If a researcher needs to centralize and keep organized all mateials in a logic structure, he is spending time that could be used to produce results.

To allow this directory to support all these utilities, different subdirectories are created under it. In these directories are defined the input and output. Bellow the structure of the data directory is presented:

    data directory
        ├── derived_data
        └── raw_data
            ├── landsat8_data
            ├── sentinel2_data
            ├── scene_id_list
            └── lasrc_auxiliary_data

In which:

**raw_data**

Directory in which the input data should be stored. Its subdirectories are explained bellow.

**raw_data/landsat8_data**

In this directory, all the Landsat-8/OLI should be stored to be used by the processing *scripts*. For Landsat-8/OLI, it is expected that each scene to be separated in its own folder. As presented bellow:

```
landsat8_data
    ├── LC08_L2SP_222081_20171120_20200902_02_T1
    └── LC08_L2SP_223081_20171111_20200902_02_T1
```

The organization of the images within each scene directory should follow the format used by the **U**nited **S**tates **G**eological **S**urvey (USGS) in the distribution of the L2 (atmospherically corrected) data of the Collection-2 (C2). Besides, the directory nomenclature, also must follow the USGS pattern (sceneid name). Errors may occur if this is not followed.

Bellow an example of how these directories must be organized internally:

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

In this directory, all the Sentinel-2/MSI should be stored to be used by the processing *scripts*. For Sentinel-2/MSI, it is expected that each scene to be separated in its own folder. As presented bellow:

```
sentinel2_data
    ├── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
    └── S2B_MSIL1C_20171122T134159_N0206_R124_T22JBM_20171122T200800.SAFE
```

The organization of the images within each scene directory should follow the format used in `.SAFE` by ESA. Besides, the directory nomenclature, also must follow the `.SAFE` pattern (sceneid name). Errors may occur if this is not followed.

Bellow an example of how these directories must be organized internally:

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

This directory contains two files: `landsat8_data` and `sentinel2_data`, which contains a list of all sceneids should be considered in the processing steps.

`scene_ids_lc8.txt`: Definition file that lists which Landsat-8/OLI on the Landsat-8 directory (`landsat8_data`) should be processed;
`scene_ids_s2.txt`: Definition file that lists which Sentinel-2/MSI on the Sentinel-2 directory (`sentinel2_data`) should be processed;

In both files, are listed the scene names that will be considered during the processing step. To exemplify its use, consider the following `landsat8_data` and `sentinel2_data` directories:

```
landsat8_data
    ├── LC08_L2SP_222081_20171120_20200902_02_T1
    └── LC08_L2SP_223081_20171111_20200902_02_T1

sentinel2_data
    ├── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
    └── S2B_MSIL1C_20171122T134159_N0206_R124_T22JBM_20171122T200800.SAFE
```

In order to use these files in the processing*scripts*, the definition files must be filled as follow:

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

The directories that are not listed in these files will not be considered during the processing step.

**raw_data/lasrc_auxiliary_data**

In this directory the auxiliary files for the LaSRC atmospheric corrections are organized. The organization follow the [USGS dissemination FTP](https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/). Bellow an example of its structure:

```
lasrc_auxiliary_data
    ├── CMGDEM.hdf
    ├── LADS
    ├── LDCMLUT
    ├── MSILUT
    └── ratiomapndwiexp.hdf
```

Note that for the processing, only the `lasrc_auxiliary_data/LADS` must be altered. This directory may contain onle the auxiliary files for the dates of the sceneids. To examplify. consider the directory `sentinel2_data`:

```
sentinel2_data
    ├── S2B_MSIL1C_20171119T133209_N0206_R081_T22JBM_20171120T175608.SAFE
    └── S2B_MSIL1C_20171122T134159_N0206_R124_T22JBM_20171122T200800.SAFE
```

To process both images in this directory using the LaSRC by executing the *scripts*, in the `LADS` directory two files reffering to the sceneid dates must be available. In this case:

```
lasrc_auxiliary_data
    ├── CMGDEM.hdf
    └── LADS
       └── 2017
           ├── L8ANC2017323.hdf_fused
           └── L8ANC2017326.hdf_fused
```

**derived_data**

This directory stores the generated results. At the end of the execution of the processing *script*, will have the following structure:

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

Where:

*Landsat-8/OLI data*

- `l8/lc8_nbar_angles`: Angle bands generated for the Landsat-8/OLI data;

- `l8/lc8_nbar`: NBAR products generated with the Landsat-8/OLI data.

*Sentinel-2/MSI LaSRC data*

- `s2/s2_lasrc_sr`: Sentinel-2/MSI data corrected for atmoshperic effects using the LaSRC;

- `s2/s2_lasrc_nbar`: NBAR products generated using Sentinel-2/MSI data corrected by LaSRC (the same `s2/s2_lasrc_sr` directory).

*Sentinel-2/MSI Sen2Cor data*

- `s2/s2_sen2cor_sr`: Sentinel-2/MSI data corected for atmospheric effects using the Sen2cor;

- `s2/s2_sen2cor_nbar`: NBAR products generated using Sentinel-2/MSI data corrected by Sen2Cor (The same `s2/s2_sen2cor_sr` directory).
