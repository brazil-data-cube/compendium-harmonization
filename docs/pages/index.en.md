*[RC]: Research Compendium

### Evaluating Landsat-8 and Sentinel-2 Nadir BRDF Adjusted Reflectance (NBAR) on South of Brazil through a Reproducible and Replicable Workflow

[![rc](https://img.shields.io/badge/research%20compendium-ready-brightgreen)](#)

This is the official `Research Compendium` (RC) documentation, with all the materials (Codes, data, and computing environments) needed for the reproduction, replication, and evaluation of the results presented in the paper:

!!! quote ""

    Marujo *et al* (2022). `Evaluating Landsat-8 and Sentinel-2 Nadir BRDF Adjusted Reflectance (NBAR) on South of Brazil through a Reproducible and Replicable Workflow`. This Paper will be submitted in June 2022.

#### Research Compendium Content

The organization defined for this RC, aims to facilitate the use of the codes implemented to generate the results presented in the article. The processing codes are made available in a structure of [examples](/en/reproducible-research/) that allow the execution without difficulties, making it possible for others to reproduce and replicate the study performed.

These codes are stored in the `analysis` directory, which has three subdirectories:

- [:file_folder: analysis/notebook](analysis/notebook): Directory with the Jupyter Notebook version of the processing flow implemented in the article associated with this RC. For more information, see the Reference Section [Processing Scripts](/en/tools/processing/);

- [:file_folder: analysis/pipeline](analysis/pipeline): Directory with the Dagster version of the processing flow implemented in the article associated with this RC. For more information, see the Reference Section [Processing Scripts](/en/tools/processing/);

- [:file_folder: analysis/data](analysis/data/): Directory for storing the generated input and output data. It contains the following subdirectories:

    - [:file_folder: examples](analysis/data/examples): Directory with the data (Input/Output) of the examples provided in this RC. For more information about the examples, see Chapter [Data Processing](/en/reproducible-research/); 

    - [:file_folder: original_scene_ids](analysis/data/original_scene_ids): Directory for storing the original scene id index files used to produce the article results. This data can be applied to the codes provided in the [analysis/notebook](analysis/notebook) and [analysis/pipeline](analysis/pipeline) directories for reproducing the article results.

By default, the input data, because of the size of the files, is not stored directly in the data directory (`analysis/data/`). Instead, as described in detail in the Reference Section [Helper scripts](/en/tools/utilitary/), they are made available in the GitHub Release Assets of the RC repository.

To build the [processing scripts](/en/tools/processing/) available in the `analysis` directory, we have created several [software libraries](/pt/tools/libraries/) and [scripts auxiliary](/en/tools/utilitary/). The source code for some of these tools is available in the `tools` directory. In this directory there are four subdirectories, namely:

- [:file_folder: tools/auxiliary-library](tools/auxiliary-library): Source code for the [research-processing](/en/tools/libraries/#research-processing-python-library-research-processing) library , which provides the high-level operations for processing the data in this RC;

- [:file_folder: tools/calculate-checksum](tools/calculate-checksum): Source code of script [calculate-checksum](/en/tools/utilitary/#calculate-checksum-e-github-asset-upload), created to calculate the checksum of the files in this RC before sharing;

- [:file_folder: tools/example-toolkit](tools/example-toolkit): Source code of the script [example-toolkit](/en/tools/utilitarian/#example-toolkit), created to facilitate the download and validation of example data from the GitHub Release Assets;

- [:file_folder: tools/github-asset-upload](tools/github-asset-upload): Source code of the script [github-asset-upload](/en/tools/utilitary/#calculate-checksum-e-github-asset-upload), created to facilitate the upload of example data to the GitHub Release Assets.

Another directory available in this RC is `composes`. In this directory are [Docker Compose](https://docs.docker.com/compose/) configuration files for the computing environments needed to run the examples available in this RC. For more information about the RC computing environments, see the Reference Section [Computing Environments](/environment/).

In the `composes` directory, there are two subdirectories:

- [:file_folder: composes/minimal](composes/minimal): Directory with the Docker Composes to run the [Minimal example](/en/reproducible-research/minimal-example/) provided in this RC;

- [:file_folder: composes/replication](composes/replication): Directory with the Docker Composes to run the [Replication example](/en/reproducible-research/replication-example/) provided in this RC.

For more information about the examples, see Section [Data Processing](/en/reproducible-research/).

Complementary to the `composes` directory is the `docker` directory. This directory holds the [Dockerfile](https://docs.docker.com/engine/reference/builder/) files used to build the environments used in Docker Composes. This directory has two subdirectories:

- [:file_folder: docker/notebook](docker/notebook): Directory with the [Dockerfile](https://docs.docker.com/engine/reference/builder/) of the environment required for [running the Jupyter Notebook version](/environment/#jupyter-notebook) of this RC process stream.

- [:file_folder: docker/pipeline](docker/pipeline): Directory with the [Dockerfile](https://docs.docker.com/engine/reference/builder/) of the environment needed for [running the Dagster version](/en/tools/environment/#dagster) of this RC process stream.

In addition to these directories, some files are fundamental to using the materials in this RC:

- [Vagrantfile](Vagrantfile) and [bootstrap.sh](bootstrap.sh): [Vagrant](https://www.vagrantup.com/) files used to build a virtual machine with the complete environment for running the [Processing scripts](/en/tools/processing/) available in the `analysis` directory. For more information, see the reference section [Computing Environments - Virtual Machine with Vagrant](/en/tools/environment/#virtual-machine-with-vagrant);

- [Makefile](Makefile): `GNU Make` definition file to make the use of the materials available in the `analysis` and `composes` directories easier. The [setenv.sh](setenv.sh) file is used by `Makefile` to define the user who will run Jupyter Notebook environment. More information is provided in Section [Data Processing](/en/reproducible-research/).
