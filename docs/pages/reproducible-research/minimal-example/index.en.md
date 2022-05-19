*[RC]: Research Compendium

# Minimal example

!!! attention "Requirements"

    Before starting this example, certify that the [requirements](/en/reproducible-research/#requirements) are installed in your work environment.

Alongside this RC, there is an article in which the harmonization experiments were conducted using Landsat-8/OLI and Sentinel-2/MSI images. As presented in
the [Reference Chapter](/en/tools/), the materials and tools of this RC, represent the effort of generating the mentioned article results.

In this section, these materials and a reproducible example are presented, going through all the processing chain used in the article to generate the harmonized products. This minimal example consists in a small *subset* containing 4 scenes (`2x Landsat-8/OLI` and `2x Sentinel-2/MSI`) extracted from the original dataset.

With this minimal example it is expected to allow researchers to explore the produced material and the chain implementation of the article.

!!! tip "Reference"

    This is a practical section, in which the RC materials are used. If you need more info regarding the used tools, please consult the [Reference Chapter](/en/tools/).

## Research Compendium Download

This example first step is to *download* this RC and all its materials. To do this, in a terminal, use `git` to [clone](https://git-scm.com/docs/git-clone):

``` sh
git clone https://github.com/brazil-data-cube/Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance
```

After the [clone](https://git-scm.com/docs/git-clone), a new directory will be created in your current directory. Its name is `Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance`:

``` sh
ls -ls .

#> 4 drwxrwxr-x 3 ubuntu ubuntu 4096 May  2 00:44 Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance
```

Now, access the directory `Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance` and list its content:

*Changing directory*
``` sh
cd Evaluating-Landsat-8-and-Sentinel-2-Nadir-BRDF-Adjusted-Reflectance
```

*Listing its content*

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

As you can see, the content of this directory are the materials of this RC. This will be the base files used in this tutorial. The description of each directory of this RC can be found in the [Introduction](/en/#research-compendium-organization) of this documentation.

## Download the data

After downloading the RC, one can follow the steps presented in the introduction of the ([Data Processing](/en/reproducible-research/#data-processing)) chapter to download the files that will be used in this example. These data are described in the [Example Toolkit](/en/tools/utilitary/#example-toolkit) section and are stored in the [GitHub Release Assets](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

It will be required to use the [Example Toolkit](/en/tools/utilitary/#example-toolkit) to obtain them. This tool downloads and organizes the data in the structure required by the [processing scripts](/en/tools/processing/#diretorio-de-dados).

To execute it, first create a Docker network, in which the Containers created in this tutorial will be associated to. To do that, in your terminal, use the following command:

``` sh
docker network create research_processing_network

#> fdaa46b4fe70bd34b6cb0e59734376234d801599a1fb1cbe1d9fd66a8f5044b1
```

Now, through your `GNU Make`, execute the following command `example_download_data`:

``` sh
make example_download_data
```

!!! tip "Pro tip"

    During the `GNU Make` execution, if you have any problema regarding permissions on the execution of the `setenv.sh` file, use the following command before executing the `GNU Make` again:

    ``` sh
    chmod +x setenv.sh
    ```

This command will use a Docker Compose to *download* the example data. After executing, the data *download* will start and a message similar to the one bellow will be presented (A few fields are omitted here so the documentation can be more readable):

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

!!! tip "Data download"

    If you are interested in obtaining more information regarding the data *download*, please, consult the reference section [Auxiliary scripts](/en/tools/utilitary/#scripts-auxiliares).

Following the RC [organization](#), the downloaded data were stored in the directory `analysis/data/examples/minimal_example/raw_data/`:

``` sh
ls -ls analysis/data/examples/minimal_example/raw_data/

#> total 16
#> 4 drwxrwxrwx 4 root root 4096 May  2 01:25 landsat8_data
#> 4 drwxrwxrwx 5 root root 4096 May  2 01:22 lasrc_auxiliary_data
#> 4 drwxrwxrwx 2 root root 4096 May  2 01:22 scene_id_list
#> 4 drwxrwxrwx 4 root root 4096 May  2 01:25 sentinel2_data
```

!!! tip "Data organization"

    The data organization in the directory `analysis/data/examples/minimal_example/raw_data/` follow the processing *scripts* required pattern. For more information, please, consult the reference section [Data Directory](/en/tools/processing/#data-diretory).


## Processing data through Jupyter Notebook

Continuing the processing chain presented in the [Chapter Indroduction](/en/reproducible-research/), a first way to execute the processings described in the article associated with this RC, is through a Jupyter Notebook. This document has the detailed description of each step of the processing chain. In this example, the notebooks will be the first approach.

!!! tip "Jupyter Notebook everywhere"

    For more information regarding this RC Jupyter Notebooks, consult the section [Processing scripts - Jupyter Notebook](/en/tools/processing/#jupyter-notebook).

To use the notebooks and process the data, you can use the command `example_notebook` through the `GNU Make`. This command will configure the Container in order to you execute the Jupyter Notebook through an interface [Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/):

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

Once this command is executed, your terminal will show the address to access the Jupyter Lab through a web interface. Use your browser to access the following address:

``` sh
firefox http://127.0.0.1:8888/lab?token=e6ad88f2a1b6358e1de88ea5a99ba3fd0b872293d3c9e845
```

After accessing it, access the processing file that is in the following directory structure: `analysis > notebook > research-processing.ipynb`.

To exemplify this process, bellow, there is a video of the mentioned steps:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/harmonization-jupyter.gif){ width="1024" }
  <figcaption>Jupyter Notebook configuration to process the data</figcaption>
</figure>

After the execution, the generated products will be available on the directory `analysis/data/derived_data`

!!! tip "Removing data"

    After the tests, if you wish, you can remove the input/output data, so it does not use your disk volume. Through the `GNU Make` execute the command `example_cleanup_data`:

    ``` sh
    make example_cleanup_data
    ```

    This will erase all the data. Doing this, the next execution will require to *download* again the files.

## Processing through Dagster

The second approach to process the downloaded data is using Dagster. With this tool, the processing of the data is performed as *batch*.

!!! tip "More Dagster"

    For more informationg regarding this RC Dagster, consult the section [Processing scripts - Dagster](/en/tools/processing/#dagster).

To use Dagster and process the data, use the command `example_pipeline` through the `GNU Make`. This command will configure the Container so you can access DagIt through interface [DagIt](https://docs.dagster.io/0.12.15/concepts/dagit/dagit):

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

Once this command is executed, your terminal will show the adress to access Dagster. Use your browser to navegate and access the following address:

``` sh
firefox http://127.0.0.1:3000
```

!!! note "Pro tip"

    The address presented in the terminal is `0.0.0.0` and the access is through the address `127.0.0.1` in the above example. This is possible since, `0.0.0.0` means that any address can access the created service.


Accessing the address you will be at DagIt and can start processing data. The Figure bellow shows an example of the DagIt you will see:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-01.svg){ width="1024" }
  <figcaption>DagIt example interface.</figcaption>
</figure>

To start processing data ib DagIt, select the option `Playground`:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-02.svg){ width="1024" }
  <figcaption>DagIt's interface Playground Option.</figcaption>
</figure>

Acessing the `Playground` tab you will see a field containing the configuration definitions that should be considered during processing. This configuration is used to determine which will be the inputs, auxiliary data and also the output in which data will be written. These options must be defined in order to consider the downloaded data.

The Figure Bellow presents a field in which the configurations are set.

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-03.svg){ width="1024" }
  <figcaption>DagIt configuration field.</figcaption>
</figure>

To auxiliate in this configuration, during the data download (Subsection [Data Download](/en/reproducible-research/minimal-example/#data-download)), the *script* [Example toolkit](/en/tools/utilitary/#example-toolkit) also generated the Dagster configuration required to use the data. This file is available at the directory `analysis/pipeline/`, with the name `config.yaml`.

!!! note "Dagster Configuration and Example toolkit"

    For more information regarding the Dagster configuration format and how it can be adapted to your context, please, see the reference section [Dagster - Configuration](/en/tools/processing/#configuration_1).

    If you wish to understand how [Example toolkit](/en/tools/utilitary/#example-toolkit) works, consult the reference section [Auxiliary scripts](/en/tools/utilitary/#scripts-auxiliares).

Copy the content of the `config.yaml` file and paste it on the DagIt configuration interface field:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/dagit-interface-04.svg){ width="1024" }
  <figcaption>DagIt configuration field (Filled).</figcaption>
</figure>

Once this, start the processing by clicking `Launch Execution`.

To exemplify each of these steps, bellow you can find a video with each of the configuration steps and use of Dagster:

<figure markdown>
  ![libs-link](/assets/reproducible-research/minimal-example/harmonization-dagster.gif){ width="1024" }
  <figcaption>Dagster configuration to process the data</figcaption>
</figure>

After the execution, the generated products will be available on the directory `analysis/data/derived_data`.

!!! tip "Removing Data"

    After the tests, if you wish, you can remove the input/output data, so it does not use your disk volume. Through the `GNU Make` execute the command `example_cleanup_data`:

    ``` sh
    make example_cleanup_data
    ```

    This will erase all the data. Doing this, the next execution will require to *download* again the files.
