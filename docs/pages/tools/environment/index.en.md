*[RC]: Research Compendium
*[CLI]: Command-Line Interface

# Computational Environments

Behind each step on the [processing scripts](/en/tools/processing/), as presented in the previous sections, there are several tools and *software* libraries being used.

Some of these tools use special technologies to execute their operations, as is the case for the [research-processing library](/en/tools/libraries/#research-processing-python-library-research-processing), that uses Docker Containers to execute the processing functions in isolated environments. Other tools only use their own environment, as for the auxiliary *script* [Example toolkit](/en/tools/utilitary/#example-toolkit). In this case, it is required that its own environment to be configured to execute the *script*.

In both presented scenaries, there are specific challenges on managing the used computational environment. For instance, specific configurations may be required on the *software* to operate alongside the [research-processing library](/en/tools/libraries/#research-processing-python-library-research-processing), while specific configurations may be required during the [Example toolkit](/en/tools/utilitary/#example-toolkit) use.

To solve these problems and avoud that the configuration used to interfere with reproductibility and replicability of the [processing scripts](/en/tools/processing/) created in this RC, all the environments required for using the tools were organized in Docker images. These, represent "environment packages" ready to use, in which all dependencies and required configurations are already set.

In this section each Docker Image is presented, its characteristics, configuration and use. Note that these images were not created for a specific environment, as long as it supports Docker, any operational system can be used. However, in this documentation, Linux Ubuntu 20.04 syntax was adopted. Thus, changes can be required on the commands if you wish to use a different operational system, e.g. Windows.


!!! note "Changes between operational systems"


    Although we believe that the commands and hints in this document can be used without trouble in Linux operational systems (e.g., Ubuntu, Debian) and MacOS, there is no warranty that this will always be true. Besides, for those who use Windows, changes in the commands may be required.

    To enable the use of the materials produced here even in those environments, we also created a Ubuntu 20.04 Virtual Machine, containing all required dependencies (e.g., [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/)) to enable that all the commands presented here could be used.

    If you need to use this Virtual Machine, please, consult the Section [Virtual Machine with Vagrant](/en/tools/environment/#vagrant-virtual-machine).


## Docker Images <img src="/assets/tools/environment/docker/docker-logo.png" align="right" width="160"/>

In this RC, there are different types of environments that are being configured within the Docker Images, which can be categorized in two types:

**Executable**

Command Line Interfaces (CLI) are simple and direct to use, allowing automation during the processing steps. The `Executable`  Docker Images are the images created to store a *script* that can be executed as a CLI. For that, this type of Docker Image has the following properties:

1. Each Docker Image execution represents an individual execution of the tool it is associated;
2. Parameters can be passed during a Docker Image execution. These parameters are used to configure the executed tool;
3. Docker Volumes and environmental variables, also can be used to configure a Docker Image, being used to determine the inputs, outputs and configurations of the executed tool.

**Environment**

Different from the `Executable` Docker Images, these Docker Images are created to serve a complete environment that will be used to execute the tool, as a Jupyter Notebook or a Dagster Web Interface.

The main difference between these two types of Docker Images created in this RC is its goals. While the `Executables` represent the executable tools, the `Environment` represent their environment, used to execute these specific tools.

In the following Subsections, the Docker Images created in this RC are presented.

### Sen2Cor 2.9.0
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/en/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/sen2cor)

[Sen2cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/) is an atmospherical correction processor developed for Sentinel-2 products. As inputs it uses Top of Atmosphere (ToA) radiance Sentinel-2 products, also called Level-1C (L1C) and generates "Bottom of the atmosphere (BOA) reflectance" products, also providing a Scene Classification Layer (SCL), that has several classes, including cloud, cloud shadow and snow.

!!! note "More about Sen2Cor"

    For more information regarding Sen2Cor, consult the [oficial User Manual](http://step.esa.int/thirdparties/sen2cor/2.9.0/docs/S2-PDGS-MPC-L2A-SRN-V2.9.0.pdf).


We prepared a Docker Image with sen2cor installed to allow executions of it to be reproducible and reusable. This Docker Image, named `sen2cor`, has all its dependencies and configurations required in order to execute the Sen2Cor.

!!! note "Sen2cor Versions"

    The [Sen2Cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/), is a *software* maintained by [**E**uropean **S**pace **A**gency](https://www.esa.int/) (ESA) and continues in development with new versions being released. In this RC, the Sen2cor version `2.9.0` was used.

The following topics, present the main characterisctis of this Docker Image, as volumes, auxiliary data and how to use it.

**Auxiliary Data**

To execute the `sen2cor`, it is required to obtain some auxiliary data. The [ESACCI-LC for Sen2Cor data package](http://maps.elie.ucl.ac.be/CCI/viewer/download.php), which is used to identify clouds and classify a scene. It can be obtained following the steps listed bellow:

1. Access the address: [http://maps.elie.ucl.ac.be/CCI/viewer/download.php](http://maps.elie.ucl.ac.be/CCI/viewer/download.php);
2. Sign in;
3. Search for the `ESACCI-LC for Sen2Cor data package`;
4. *Download* this package (`zip` file);
5. Extract its content in a directory. It is recommended to name it `CCI4SEN2COR`.

After extracting the files, the directory will contain the following files:

- `ESACCI-LC-L4-WB-Map-150m-P13Y-2000-v4.0.tif` (GeoTIFF);
- `ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7.tif` (GeoTIFF);
- `ESACCI-LC-L4-Snow-Cond-500m-P13Y7D-2000-2012-v2.0` (Directório).

**Volumes**

To use the `Sen2cor`, it is required to define a few Docker Volumes. These volumes specify the input, output, configuration files and auxiliary files used by the tool. Bellow these volumes are listed and descripted:


`Input data` (Required)

:   Directory containing the input files. This volume should map a directory in the local machine to the Container `/mnt/input_dir` directory. It is recommended to use a read-only volume, to ensure no modification to be made on the input data.


`Output directory` (Required)

:   Directory in which the output products will be stored. This volume should map a directory in the local machine to the Container `/mnt/output_dir` directory.


`Auxiliary data` (Required)

:   Directory containing the auxiliary files, required by Sen2cor. This volume should map a directory in the local machine to the Container `/mnt/sen2cor-aux/CCI4SEN2COR`.

`Configuration file` (Optional)

:   Volume that defines a configuration file (`L2A_GIPP.xml`). This volume should map a `L2A_GIPP.xml` file in the local machine to the Container `/opt/sen2cor/2.9.0/cfg/L2A_GIPP.xml`.

`SRTM data` (Opcional)

:   Volume to store SRTM data used by Sen2cor. This volume should map a directory in the local machine to the Container `/mnt/sen2cor-aux/srtm`.

**Use example (Docker CLI)**

The following code presents, through Docker CLI, an example on how to use the Docker Image `sen2cor` to process a single scene.

!!! tip "Image name"

    On the following command, the Docker Image `sen2cor` is identified as `marujore/sen2cor:2.9.0` stored in the user [marujore](https://hub.docker.com/u/marujore) on DockerHub, being the chosen version `2.9.0`.

!!! warning "Command format"

    The following command was created to be didatic. If you desire to use it, don't forguet to replace its values and remove the blank spaces between lines.O comando abaixo é criado para ser ditádico.

``` sh
docker run --rm \

    # Volume: Input data
    --volume /path/to/input_dir:/mnt/input_dir:ro \

    # Volume: Output Data
    --volume /path/to/output_dir:/mnt/output_dir:rw \

    # Auxiliary Data: Diretório CCI4SEN2COR
    --volume /path/to/CCI4SEN2COR:/mnt/aux_data \

    # Configuration file: L2A_GIPP.xml (Opcional)
    --volume /path/to/L2A_GIPP.xml:/opt/sen2cor/2.9.0/cfg/L2A_GIPP.xml \

    # SRTM Data (Opcional)
    --volume /path/to/srtm:/root/sen2cor/2.9/dem/srtm \

    # Docker Image and scene to be processed
    marujore/sen2cor:2.9.0 S2A_MSIL1C_20210903T140021_N0301_R067_T21KVR_20210903T172609.SAFE
```

The execution of the command presented above will create a `sen2cor` Docker Container. This Docker Container will process the `S2A_MSIL1C_20210903T140021_N0301_R067_T21KVR_20210903T172609.SAFE` scene. Note that in this command, the input directory (`/path/to/input_dir`) must contain a subdirectory with the scene `S2A_MSIL1C_20210903T140021_N0301_R067_T21KVR_20210903T172609.SAFE`.

For more information, consult the [GitHub Repository](https://github.com/brazil-data-cube/sen2cor-docker), where the versioning of the changes in this Docker Image (`sen2cor`) has been keep.

### LaSRC 2.0.1
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/en/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/lasrc)

[LaSRC](https://ntrs.nasa.gov/api/citations/20190001670/downloads/20190001670.pdf) is an atmospheric correction processor, originally proposed for the Landsat-8 Collection 1, and posteriorly adapted to also correct Sentinel-2 products. It uses as input Landsat-8 Digital Number products (DN) or Sentinel-2 Top of Atmosphere (ToA) radiance products, also called Level-1C (L1C). As results this tool generates surface reflectance (SR) products.

To facilitate the use of LaSRC in this RC, and ensure the executions to be reproducible and reusable, we created a Docker image for the LaSRC, called `lasrc`. The `lasrc`, has all dependencies and configuration required to execute the LaSRC processor.

The following topics present the main characteristics of this Docker Image, as volumes, auxiliary data and how to use it.

**Auxiliary data**

To execute `lasrc`, it is required to define a few auxiliary data. To obtain then see the following steps:

1. Access: [https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/](https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/);
2. Download all the available contents, except the `LADS` folder.

`LADS` data is also required to use the LaSRC. However, this directory contains daily files since 2013 until nowadays, which is a huge volume of data. To perform this RC experiment, you can *download* the `LADS` accordingly to the dates of the data you will process.

!!! tip "LADS files selection"

    Each LADS file links to a day of the year. Thus, to process the image from January first 2017, one can obtain the LADS `L8ANC2017001.hdf_fused` in 2017, which is represented by `001` in the day of the year format.

At the end of the acquisition, the auxiliary data directory must follow this structure:

```
.
├── CMGDEM.hdf
├── LADS
├── LDCMLUT
├── MSILUT
└── ratiomapndwiexp.hdf
```

**Volumes**

To use the `lasrc`, it is required to define a few Docker Volumes. These volumes, specify the input data, output data and auxiliary files used by the tool during processing. Bellow, is descripted each volume that must be created during the execution of LaSRC Docker Image:

`Input data` (Required)

:   Directory containing the input data. This volume should map a directory in the local machine to the Container `/mnt/input_dir` directory. It is recommended to use a read-only volume, to ensure no modification to be made on the input data.

`Output data` (Required)

:   Directory containing the output data. This volume should map a directory in the local machine to the Container `/mnt/output_dir` directory.


`Auxiliary data` (Required)

:   Directory containing the auxiliary data required by LaSRC. The created volume, should map a directory in the local machine to the Container `/mnt/atmcor_aux/lasrc/L8` directory.

**Use example (Docker CLI)**

The codes bellow present two examples on how to use `lasrc`, through the Docker CLI. On the first example, a Landsat-8/OLI scene is processed, while on the second a Sentinel-2/MSI image is processed.

!!! tip "Image name"

    On the following commands, a `lasrc` Docker Image is identified as `marujore/lasrc:2.0.1`, stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub.

!!! warning "Command format"

    The following command was created to be didatic. If you desire to use it, don't forguet to replace its values and remove the blank spaces between lines.O comando abaixo é criado para ser ditádico.

*LaSRC Landsat-8/OLI example*

``` sh
docker run --rm \

    # Volume: Input data
    --volume /path/to/input/:/mnt/input-dir:rw \

    # Volume: Output data
    --volume /path/to/output:/mnt/output-dir:rw \

    # auxiliary data (data L8/LADS)
    --volume /path/to/lasrc_auxiliaries/L8:/mnt/atmcor_aux/lasrc/L8:ro \

    # Docker Image and scene to be processed
    --tty brazildatacube/lasrc:2.0.1 LC08_L1TP_220069_20190112_20190131_01_T1
```

*LaSRC Sentinel-2/MSI example*

``` sh
 docker run --rm \

    # Volume: Input data
    --volume /path/to/input/:/mnt/input-dir:rw \

    # Volume: Output data
    --volume /path/to/output:/mnt/output-dir:rw \

    # auxiliary data (data L8/LADS)
    --volume /path/to/lasrc_auxiliaries/L8:/mnt/atmcor_aux/lasrc/L8:ro \

    # Docker Image and scene to be processed
    --tty brazildatacube/lasrc:2.0.1 S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE
```

As can be noted, the difference on using `lasrc` for different satellite-sensors relly only on the sceneid name. It is important to note that, for both cases, the input directory (`/path/to/input/`) must contain the scenes to be processed. In this case `LC08_L1TP_220069_20190112_20190131_01_T1` and `S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE`.

For more information, consult the [Github repository](https://github.com/brazil-data-cube/lasrc-docker), where the versioning of the changes in this Docker Image (`lasrc`) has been keep.

### L8Angs
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/en/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/l8angs)

[Landsat Ang Tool](https://www.usgs.gov/landsat-missions/landsat-tools) is a tool developed and maintained by [**U**nited **S**tates **G**eological **S**urvey](https://www.usgs.gov/). This tool uses the `ANG.txt` that are provided alongside Landsat-8 images and use them to generate per *pixel* angle bands. The angle bands are solar azimuth angle (`SAA`), solar zenithal angle (`SZA`), view azimuth angle (`VAA`) and view zenithal angle (`VZA`). The bands are generated with the same resolution as OLI soectral bands (30m).

!!! note "More about Landsat Ang Tool"

    For more information regarding  Landsat Ang Tool, consult the [USGS official page about the tool](https://www.usgs.gov/core-science-systems/nli/landsat/solar-illumination-and-sensor-viewing-angle-coefficient-files?qt-science_support_page_related_con=1#qt-science_support_page_related_con).

In this RC, the Landsat-8/OLI (Collection-2) images were obtained already processed to Surface Reflectance Level (L2). However, for further processing we use the angle bands, using the [Landsat Ang Tool](https://www.usgs.gov/landsat-missions/landsat-tools).

The installation and configuration of the [Landsat Ang Tool](https://www.usgs.gov/landsat-missions/landsat-tools) can make hard to replicate and reproduce this experiment in the future. Due to that, in this RC we created a Docker Image, named `l8angs`, containing the tool.

The following topics present the main characteristics of this Docker Image, as volumes and auxiliary data to its execution, as well as Docker CLI execution examples.

**Volumes**

To use `l8angs`, you must provide the following volume during the execution:

`Input data` (Required)

:   The created volume, should map a directory in the local machine to the Container `/mnt/input-dir` directory. The angle bands are generated on the same input directory, this is the standard behavior of the tool.

**Use example (Docker CLI)**

The code bellow, presents a use example of the `l8angs` through Docker CLI.

!!! tip "Image name"

    In the following commands, the `l8angs` Docker image, identified as `marujore/l8angs:latest` on DockerHub.

!!! warning "Command format"

    The following command was created to be didatic. If you desire to use it, don't forguet to replace its values and remove the blank spaces between lines.O comando abaixo é criado para ser ditádico.

``` sh
docker run --rm \

    # Volume: Input data
    -v /path/to/input/:/mnt/input-dir:rw \

    # Docker Image and scene to be processed
    marujore/l8angs:latest LC08_L2SP_222081_20190502_20200829_02_T1
```

The execution of the command presented above will create a `l8angs` Docker Container. This Docker Container will process the `LC08_L2SP_222081_20190502_20200829_02_T1` scene. In this command, the input dir (`/path/to/input/`) must contain a subdirectory named `LC08_L2SP_222081_20190502_20200829_02_T1`, which is the scene being processed.

For more information, consult the [GitHub repository](https://github.com/marujore/landsat-angles-docker), which contains the versioning and changes made on `l8angs`.

### Sensor Harm
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/en/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/nbar)

In this RC, the Landsat-8 Collection-2 images were already obtained as surface reflectance products (L2) while Sentinel-2 images were obtained as L1C and processed using Sen2cor or LaSRC. Both Landsat-8 and Sentinel-2 images are harmonized using the [sensor-harm](/en/tools/libraries/#sensor-harmonization-python-library-sensor-harm) library. To allow reproductibility and replicability of this tool use, we created a Docker Image called `nbar`. In this image, all dependencies and configurations to execute [sensor-harm](/en/tools/libraries/#sensor-harmonization-python-library-sensor-harm) are already prepared.

The following topics present the main characteristics of this Docker Image, the volumes it requires and use examples.

**Volumes**

To use the `nbar`, it is required to define some Docker Volumes. These volumes specify the input and auxiliary data used by sensor-harm. Bellow a list of these volumes is listed and descripted:

`Input data` (Required)

:   Directory containing the input data. This volume should map a directory in the local machine to the Container `/mnt/input_dir` directory. It is recommended to use a read-only volume, to ensure no modification to be made on the input data.


`Output data` (Required)

:   Directory containing the output data. This volume should map a directory in the local machine to the Container `/mnt/output_dir` directory.


`Angle directory` (Required only for Landsat-8/OLI)

:   Directory containing the angles of the scene that will be processed. The created volume, should map a directory in the local machine to the Container `/mnt/angles-dir` directory. It is recommended to use a read-only volume, to ensure no modification to be made on the input data.


**Use example (Docker CLI)**

The codes bellow present two examples on how to use `nbar` through Docker CLI. In the first example, the processing is performed on a Landsat-8/OLI scene, while on the second a Sentinel-2/MSI scene is used.

!!! tip "Image name"

    On the following commands, a `nbar` Docker Image is identified as `marujore/nbar:latest`, stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub.

!!! warning "Command format"

    The following command was created to be didatic. If you desire to use it, don't forguet to replace its values and remove the blank spaces between lines.O comando abaixo é criado para ser ditádico.

*Landsat-8/OLI example*

``` sh
docker run --rm \

    # Volume: Input data
    --volume /path/to/input/:/mnt/input-dir:ro \

    # Volume: Output data
    --volume /path/to/output:/mnt/output-dir:rw \

    # Angle directory (Only for Landsat-8/OLI)
    --volume /path/to/angles:/mnt/angles-dir:ro \

    # Docker Image and scene to be processed
    --tty marujore/nbar:latest LC08_L1TP_220069_20190112_20190131_01_T1
```

*Sentinel-2/MSI example*

``` sh
docker run --rm \

    # Volume: Input data
    --volume /path/to/input/:/mnt/input-dir:ro \

    # Volume: Output data
    --volume /path/to/output:/mnt/output-dir:rw \

    # Docker Image and scene to be processed
    --tty brazildatacube/sensor-harm:latest S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE
```

As can be noted, the difference on using `nbar` for different satellite-sensors relly only on the sceneid name. It is important to note that, for both cases, the input directory (`/path/to/input/`) must contain the scenes to be processed. In this case `LC08_L1TP_220069_20190112_20190131_01_T1` and `S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE`

For more information, consult the [Github repository](https://github.com/brazil-data-cube/sensor-harm), where the versioning of the changes in this Docker Image (`nbar`) has been keep.

### Processing scripts Docker Images

As presented in the [Processing scripts](/en/tools/processing/) section, two environments were created to execute this RC methodology experiments. Oe uses [Jupyter Notebook](/en/tools/processing/#jupyter-notebook), which is useful for interactive processing of the codes. The second, using [Dagster](/en/tools/processing/#dagster), which is useful for batch execution and error control.

To facilitate the use of both approaches, Docker Images were created containing the required environments of each execution. This avoids dependencies to be installed or configured to execute the [processing scripts](/en/tools/processing/).

The following topics present the Docker Images characteristics, required volumes, configuration and use example.

!!! tip "Scripts behavior"

    If you wish to reuse these Docker Images, it is recomended first to read about how is the [ processing scripts behavior](/en/tools/processing/), as well as the [software libraries](/en/tools/libraries/) used by these *scripts*.

#### Jupyter Notebook
[![docker-image-type](https://img.shields.io/badge/Type-Environment-orange)](/en/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/#)

To execute the Jupyter Notebook version, we created the `research-processing-jupyter` Docker Image. This Docker Image brings a [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/), with the required Python dependencies to execute the *scripts*. Besides, in this Docker Image, Docker is also installed, allowing the *scripts* to operate and create other processing Docker Containers.

!!! note "Environment Base"

    The creation of `research-processing-jupyter` was made using the [jupyter/minimal-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-minimal-notebook) Docker Image, made available by the [Jupyter](https://jupyter.org/) development team.

    So, all the [environment variables and configurations](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html) available on the `jupyter/minimal-notebook`  Docker Image are also applyable to `research-processing-jupyter`.

On the following topics the required configuration to use this Docker image is demonstrated. Examples on how to use the Docker CLI and [Docker Compose](https://docs.docker.com/compose/) are also presented.

**Environment variables**

To use the `research-processing-jupyter`, it is required to define the following environment variable:

`DATA_DIRECTORY` (Required)

:   Environmental variable that determines the directory, in the local machine, in which the downloaded data will be saved.


**Volumes**

The execution of the `research-processing-jupyter` requires two volumes to be mounted:

`Data Volume` (Required)

:   Volume containing the data. Following the processing function [execution model](/en/tools/libraries/#function-execution) used in the *scripts*, this volume will be used by functions inside the container (`Local`) or in other containers (`Containerized`). Thus, the volume mount must attend 2 requirements:

:     * The volume must be a [Bind Mount](https://docs.docker.com/storage/bind-mounts/);
:     * The volume mapping (`Bind Mount`) must have, in the local machine and in the Container, the same path defined in `DATA_DIRECTORY`.

:   With these definitions, the volume will be visible within the `research-processing-jupyter` Container and also by the auxiliary processing Containers generated during the [processing script](/en/tools/processing/) execution.

`Daemon Socket Volume` (Required)

:   To allow the scripts to generate processing Docker Containers, it is required to define the [Daemon Socket](https://docs.docker.com/engine/reference/commandline/dockerd/#description) as a volume. Doing this, the Docker within the container created with the `research-processing-jupyter` Image is capable of interacting with the local machine Docker, allowing processing Containers to be created.

**User definition**

Complementing the `Daemon Socket volume` definition, to execute the `research-processing-jupyter`, it is required to specify the user (`UID`) and group (`GID`) on the local machine that has permission to interact with the o Docker Daemon. These values will be applied to the Container standard user so Docker can allow it to also interact with the Docker Daemon of the local machine.

!!! note "Docker permission"

    If you are intereseted in understanding the detail behind this user definition, we recommend that you consult the [oficial Docker documentation](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

To define the user duering `research-processing-jupyter` execution, you can use the parameter [--user](https://docs.docker.com/engine/reference/run/#user). If you with to use the Docker Compose, the field [user](https://docs.docker.com/engine/reference/run/#user) can be used for this definition.

**Use example (Docker CLI)**

Bellow is presented an example of how to use the `research-processing-jupyter` Docker Image through the Docker CLI:

!!! tip "Image name"

    On the following commands, a `research-processing-jupyter` Docker Image is identified as `marujore/research-processing-jupyter:latest` , stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub.

!!! warning "Command format"

    The following command was created to be didatic. If you desire to use it, don't forguet to replace its values and remove the blank spaces between lines.

``` sh
docker run \
  --name research-processing-jupyter \

  # User definition
  --user ${UID}:${GID} \

  # Environment variable
  --env JUPYTER_ENABLE_LAB=yes \ # Activating JupyterLab
  --env DATA_DIRECTORY=/my-data-dir \

  # Volume: Data Volume
  --volume /my-data-dir:/my-data-dir \

  # Volume: Daemon Socket Volume
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \

  # Network port in which the service will be accessed
  --publish 8888:8888 \

  # Docker Image
  marujore/research-processing-jupyter:latest
```

!!! tip "User definition"

    To define a user, using the environment variables (`${UID}` e `${GID}`), as in the previous command, before executing the Docker command use the following commands:

    ``` sh
    export UID=`id -u $USER`
    export GID=`cut -d: -f3 < <(getent group docker)`
    ```

After the execution of the above command, a result simillar to the bellow should be presented:

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

After executing this command, using a web browser and accessing the presented JupyterLab address (Replace the address bellow by what has been showed in your terminal):

``` sh
firefox http://127.0.0.1:8888/lab?token=0497e15e042d52cfb498a2edf3d2c6e5874e79b4808ca860
```

**Use example (Docker Compose)**

Bellow, the same example performed using `Docker CLI` is presented using [Docker Compose](https://docs.docker.com/compose/). First, the `docker-compose.yml` file was created:

!!! tip "Image name"

    On the following commands, a `research-processing-jupyter` Docker Image is identified as `marujore/research-processing-jupyter:latest`, stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub as `latest`.

``` yml title="docker-compose.yml"
version: '3.2'

services:
  my-notebook:

    # User definition
    user: ${UID}:${GID}
    image: marujore/research-processing-jupyter:latest

    environment:
      # Environment variable
      - JUPYTER_ENABLE_LAB=yes
      - DATA_DIRECTORY=/my-data-dir

    volumes:

      # Volume: Data volume
      - type: bind
        source: /my-data-dir
        target: /my-data-dir

      # Volume: Daemon Socket Volume
      - type: bind
        source: /var/run/docker.sock
        target: /var/run/docker.sock

    ports:

      # Network port in which the service will be accessed
      - "8888:8888"
```

!!! tip "User definition"

    To define a user, using the environment variables (`${UID}` e `${GID}`), as presented in the `docker-compose.yml`, before executing the Docker command use the following commands:

    ``` sh
    export UID=`id -u $USER`
    export GID=`cut -d: -f3 < <(getent group docker)`
    ```

With the file created, the compose can be executed:

``` sh
docker-compose -f docker-compose.yml up
```

The output of the above command should be similar to:

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

With this information, the JupyterLab can be accesse in the browser. For that open the link displayed in your terminal on your browser:

``` sh
firefox http://127.0.0.1:8888/lab?token=6d37701a6787bd58a7f92f29f33709970df11a742bf3b79b
```

#### Dagster
[![docker-image-type](https://img.shields.io/badge/Type-Environment-orange)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](https://hub.docker.com/r/marujore/#)

To execute the Dagster version, the `research-processing-dagster`  Docker Image was created. This Docker Image has Dagster (version `0.12.15`), alongside [DagIt](https://docs.dagster.io/0.12.15/concepts/dagit/dagit), a web interface to configure and interact with Dagster. It also has a Docker installed, to allow *scripts* to create and operate other processing Docker Containers.

**Environment variables**

To use the `research-processing-dagster`, it is required to define the following environmental variable:

`DATA_DIRECTORY` (Required)

:   Environmental variable that determines the directory, in the local machine, in which the downloaded data will be saved.

**Volumes**

The execution of the `research-processing-dagster` requires the definition of the following `Docker volumes`:

`Data volume` (Required)

:   Volume containing the data. Following the processing function [execution model](/en/tools/libraries/#function-execution) used in the *scripts*, this volume will be used by functions inside the container (`Local`) or in other containers (`Containerized`). Thus, the volume mount must attend 2 requirements:

:     * The volume must be a [Bind Mount](https://docs.docker.com/storage/bind-mounts/);
:     * The volume mapping (`Bind Mount`) must have, in the local machine and in the Container, the same path defined in `DATA_DIRECTORY`.

:   With these definitions, the volume will be visible within the `research-processing-jupyter` Container and also by the auxiliary processing Containers generated during the [processing script](/en/tools/processing/) execution.

`Daemon Socket Volume` (Required)

:   To allow the scripts to generate processing Docker Containers, it is required to define the [Daemon Socket](https://docs.docker.com/engine/reference/commandline/dockerd/#description) as a volume. Doing this, the Docker within the container created with the `research-processing-jupyter` Image is capable of interacting with the local machine Docker, allowing processing Containers to be created.

**Use example (Docker CLI)**

Bellow is presented an example of how to use the `research-processing-dagster` Docker Image through the Docker CLI:

!!! tip "Image name"

    On the following commands, a `research-processing-dagster` Docker Image is identified as `marujore/research-processing-dagster:latest` stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub as `latest`.

!!! warning "Command format"

    The following command was created to be didatic. If you desire to use it, don't forguet to replace its values and remove the blank spaces between lines.


``` sh
docker run \
  --name research-processing-dagster \

  # Environment variable
  --env DATA_DIRECTORY=/my-data-dir \

  # Volume: Data Volume
  --volume /my-data-dir:/my-data-dir \

  # Volume: Daemon Socket Volume
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \

  # Network port in which the service will be accessed
  --publish 3000:3000 \

  # Docker Image
  marujore/research-processing-dagster:latest
```

After executing the above command, a result similar to the showed bellow will be displayed:

``` sh
  # (Omitted)

  Welcome to Dagster!

  If you have any questions or would like to engage with the Dagster team, please join us on Slack
  (https://bit.ly/39dvSsF).

Serving on http://0.0.0.0:3000 in process 1
```

After executting this command, use a web browser to access the DagIt adress presented:

``` sh
firefox http://127.0.0.1:3000
```

**Use example (Docker Compose)**

Bellow, the same example performed using `Docker CLI` is presented using [Docker Compose](https://docs.docker.com/compose/). First, the `docker-compose.yml` file was created:

!!! tip "Image name"

    On the following commands, a `research-processing-dagster` Docker Image is identified as `marujore/research-processing-dagster:latest` stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub as `latest`.

``` yml title="docker-compose.yml"
version: '3.2'

services:
  my-dagster:
    image: marujore/research-processing-dagster:latest

    environment:
      # Environmnet variables
      - DATA_DIRECTORY=/my-data-dir

    volumes:
      # Volume: Data volume
      - type: bind
        source: /my-data-dir
        target: /my-data-dir

      # Volume: Daemon Socket Volume
      - type: bind
        source: /var/run/docker.sock
        target: /var/run/docker.sock

    ports:
      # Network port in which the service will be accessed
      - "3000:3000"
```

Once the file is created, the compose execution can be done:

``` sh
docker-compose -f docker-compose.yml up
```

The output of the above command should look like:

``` sh
  # (Omitted)

  Welcome to Dagster!

  If you have any questions or would like to engage with the Dagster team, please join us on Slack
  (https://bit.ly/39dvSsF).

  Serving on http://0.0.0.0:3000 in process 1
```

Now accessing the base address `http://0.0.0.0:3000` displayed on the screen, access Dagster through your browser:

``` sh
firefox http://127.0.0.1:3000
```

### Example toolkit environment
[![docker-image-type](https://img.shields.io/badge/Type-Executable-brightgreen)](/pt/tools/environment/#docker-images)
[![dockerhub-badge](https://img.shields.io/badge/avaliable%20on-dockerhub-blue)](#)

To easily use the [Example toolkit](/tools/utilitary/#example-toolkit), we created a `example-toolkit-docker` Docker Image . This Docker Image, has all the required depencies to execute the `Example toolkit`.

On the following topics the required configuration to use this Docker image is demonstrated. Examples on how to use the Docker CLI and [Docker Compose](https://docs.docker.com/compose/) are also presented.

**Environment variables**

When using the `Example toolkit`, all the configurations are performed through environment variables. On the `example-toolkit-docker`, the same pattern was adopted. Thus, before executing this image, it is required to set a few environment variables. The same environment variables used for the `Example toolkit` are also valid for the `example-toolkit-docker`.

To verify the complete list of the `Example toolkit` environment variables and their explanation, consults Section [Example toolkit - Usage](/en/tools/utilitary/#usage).

**Volumes**

The execution of the `example-toolkit-docker`, requires the definition of a few Docker Volumes. These volumes, specify the input, output, configuration and auxiliary data. Bellow these volumes are presented:

`Data volume` (Required)

:   Directory in which downloaded data will be stored. This volume must be created on the same directory defined by the `DOWNLOAD_OUTPUT_DIRECTORY` environment variable (`Example toolkit` configuration).

`Dagster configuration volume` (Required)

:   Directory where the generated Dagster configuration file will be saved. This volume mus be created on the same directory defined by the `PIPELINE_DIR` environment variable (`Example toolkit` configuration).

`Download configuration volume` (Required)

:   Configuration file containing information regarding the data that will be downloaded. The file defined in this volume must be the same defined by the `DOWNLOAD_REFERENCE_FILE` (`Example toolkit` configuration).

**Use example (Docker CLI)**

Bellow the Docker Image tagged as `example-toolkit-docker` is executed:

!!! tip "Image nameNome da imagem"

    On the following commands, a `example-toolkit-docker` Docker Image is identified as `marujore/example-toolkit-docker:latest` stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub as `latest`.

!!! warning "Command format"

    The following command was created to be didatic. If you desire to use it, don't forguet to replace its values and remove the blank spaces between lines.

``` sh
docker run \
  --name example-toolkit-docker \

  # Environment variable
  --env RAW_DATA_DIR=/compendium/data/raw_data \
  --env DERIVED_DATA_DIR=/compendium/data/derived_data \
  --env PIPELINE_DIR=/compendium/config \
  --env DOWNLOAD_OUTPUT_DIRECTORY=/compendium/data \
  --env DOWNLOAD_REFERENCE_FILE=/compendium/config/example-toolkit.json \

  # Volume: Data Volume
  --volume /my-data/dir:/compendium/data \

  # Volume: Dagster configuration volume
  --volume /my-dagster/dir:/compendium/config \

  # Volume: download configuration volume
  --volume /my-toolkit/config.json:/compendium/config/example-toolkit.json \

  # Docker Image
  marujore/example-toolkit-docker:latest
```

After executing the above command, a result similar to the showed bellow will be displayed:

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

**Use example (Docker Compose)**

Bellow, the same example performed using `Docker CLI` is presented using [Docker Compose](https://docs.docker.com/compose/). First, the `docker-compose.yml` file was created:

!!! tip "Image name"

    On the following commands, a `example-toolkit-docker` Docker Image is identified as `marujore/example-toolkit-docker:latest` stored in the profile [marujore](https://hub.docker.com/u/marujore) on DockerHub as `latest`.

``` yml title="docker-compose.yml"
version: '3.2'

services:
  my-dagster:
    # Docker Image specification
    image: marujore/example-toolkit-docker:latest

    environment:
      # VEnvironmnet variables
      - RAW_DATA_DIR=/compendium/data/raw_data
      - DERIVED_DATA_DIR=/compendium/data/derived_data
      - PIPELINE_DIR=/compendium/config
      - DOWNLOAD_OUTPUT_DIRECTORY=/compendium/data
      - DOWNLOAD_REFERENCE_FILE=/compendium/config/example-toolkit.json

    volumes:
      # Volume: Data volume
      - type: bind
        source: /my-data/dir
        target: /compendium/data

      # Volume: Dagster configuration volume
      - type: bind
        source: /my-dagster/dir
        target: /compendium/config

      # Volume: Download configuration volume
      - type: bind
        source: /my-toolkit/config.json
        target: /compendium/config/example-toolkit.json

    ports:
      # Network port in which the service will be accessed
      - "3000:3000"
```

Once the file is created, the compose execution can be done:

``` sh
docker-compose -f docker-compose.yml up
```

The output of the above command should look like:

``` sh
  # (Omitted)

  Welcome to Dagster!

  If you have any questions or would like to engage with the Dagster team, please join us on Slack
  (https://bit.ly/39dvSsF).

  Serving on http://0.0.0.0:3000 in process 1
```

## Vagrant Virtual Machine <img src="/assets/tools/environment/vagrant/vagrant-logo.png" align="right" width="160"/>

This RC resources were developed, teste and used in `Linux` environment. Specifically, `Ubuntu 20.04`. Tests using `Ubuntu 20.10` were also performed. In theory, the executed codes can be adapted and used in other operational systems, e.g. `Windows` and `MacOS`.

However, it is important to note that there is no warranty all commands, configurations and dependencies will be available for other environments. Even using Docker, specific characteristics, as [Daemon Socket](https://docs.docker.com/engine/reference/commandline/dockerd/#description) may not be available.

To solve this and avoid that operational systems became a barrier to reproduce and replicate this RC material, we created a Vitrual Machine (VM). Using a VM, different from Docker, the whole system is virtualized.

This VM was created using [Vagrant](https://www.vagrantup.com/), a tool for provisioning and managing VMs, developed by [Hashicorp](https://www.hashicorp.com/). Vagrant is available for Windows, Linux, MacOS and other operational systems. With this tool, one can use a description file ([Vagrantfile](https://www.vagrantup.com/docs/vagrantfile)), and specify a complete virtual machine, considering elements such as:

* RAM quantity;
* CPU quantity;
* Operational System;
* Network;
* Installed packages.

Besides, many other configurations are available.

Using these characteristics, in this RC we created a `Vagrantfile` that specifies a `Ubuntu 20.04` VM, already prepared with the main dependencies required to use this RC's materials (e.g., Docker, Docker Compose). The machine is created with `12 GB` of RAM and `8 CPUs` by default.

!!! note "VM Resources"

    The ammount of resources define for the VM was considered using a machine with 24 GB of RAM and 12 CPUs as base. If necessary, the `Vagrantfile` can be used to change these values. To do that change the following properties in the file:

    ``` yml
    vb.memory = "12288"  # 12 GB

    vb.cpus = "8"
    ```

Vagrant supports several [Providers](https://www.vagrantup.com/docs/providers), which are tools to create the VMs. In this RC, we used the Open Source Provider [VirtualBox](https://www.virtualbox.org/).


### Vagrant Installation

To use the VM through Vagrant, first you need to install Vagrant. For that it is recommended to use the [official documentation](https://www.vagrantup.com/docs/installation).

### Using the VM through Vagrant

Once Vagrant is installed in your system, to create the VM, the first step consinsts in clonning the repository that contains this RC's materials:

``` sh
git clone https://github.com/brazil-data-cube/compendium-harmonization
```

After clonning, enter the directory `compendium-harmonization`:

``` sh
cd compendium-harmonization
```

And you will be able to see the RC's materials:

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

In these files, note that there is a `Vagrantfile` available. This file, has the specifications to create the VM. To create the VM with this file, use the following command:


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

After this execution, the VM will be created and ready to be used. In this case, to access the VM, use the command:

``` sh
vagrant ssh

#> Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.13.0-39-generic x86_64)

#>  * Documentation:  https://help.ubuntu.com
#>  * Management:     https://landscape.canonical.com
#>  * Support:        https://ubuntu.com/advantage

 # (Omitted)

#> vagrant@ubuntu:~$
```

Once the environment is accessed, you will be ready to use this RC's materials. For instance, if you desire to access the materials you made the clone to create the VM, you can access the `/compendium` directory:

*Changing directory*
``` sh
cd /compendium
```

*Listing files*
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
