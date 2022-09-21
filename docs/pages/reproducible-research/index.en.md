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

# Data Processing

!!! info

    This Chapter describes how to apply the available material of this RC. If you are intereseted in the concepts behind the materials, please, consult the Reference Chapter [Referência do Compendium](/tools/).

To produce the results of this RC, a large Earth Observation data colection was used (`~2TB`). With such volume, manage and process these data can require a lot of resources from researchers, which isn't always possible or available. Due to that, `verify`, `validate`, `reproduce` and `replicate` the materials can be difficult to perform.

To solve this problem and allow everyone to use the material we develop, understanding its implementation, organization and and used techniques, we created use examples. In these examples, all the RC materials are used alongside to build a processing chain. The data used in these examples are, *subsets* of the original set of data used to produce the article results. We also applied these examples on extra data, not presented on the article, to allow the possibility of replicating the materials of this RC.

The available examples are generic and can be used as a base to `reproduce` the article, as well as `replicate` it, only changing the input data.

!!! important "Generic and customizable examples"

    These characteristics were associated to the available examples, since during the development of the article, they were the first components to be developed. Once with the tools finished and tested, the results were generated.

    To generate the final results, the only required action was to change the input data from the examples to the complete set. With this we can say that the examples are generic and customizable to allow others datasets and regions to be processed.


## Example flux

Two examples are available on this RC:

`Minimal example`

:   Complete processing example, with all the article methodology steps. For this example, a small *subset* of data is used, from the data used in the article.

`Replication example`

:   Following the same steps of the `Minimal example`, in this example, a region different from the one used in the article is used to show the possibility of replication of the article processing chain.

Both examples consists in the same proessing steps. These, as can be seen in the Figure beloow are divided in three parts: `Data download`; `Processing (Jupyter)`; `Processing (Dagster)`

<figure markdown>
  ![Examples flow](/assets/reproducible-research/minimal-example/examples-flow.svg){ width="1024" }
  <figcaption>Example Flux</figcaption>
</figure>

In `Data download`, *download* of the required data to run the examples is performed. The data is made available through the [GitHub Release Assets](/en/tools/utilitary/#example-toolkit). After that, the available data can be used as input to the processing flux, which is implemented in [two different technologies](/en/tools/processing/), `Jupyter Notebook` and `Dagster`. Both implementation results are the same. The difference only consists in the environment the tools are make available. With the Jupyter Notebook, one can interactively execute the processing steps, while with Dagster it is executed in *batch*.

The execution of these steps is performed through Docker Composes. Each step has its own Docker Compose, so each step can be executed independently and isolated, being the data the only shared resource between them.

## Automation

All the logic behind the configuration of the Docker Composes was inserted in a `Makefile`, which contains all the commands to execute it through [GNU Make](https://www.gnu.org/software/make/).

!!! tip "Make and reproducible research"

    The idea of using `Make` came from the magnific [*The Turing Way handbook to reproducible, ethical and collaborative data science*](https://the-turing-way.netlify.app/welcome.html).

    For more details on `GNU Make` and reproducible search, consult [Reproducibility with Make](https://the-turing-way.netlify.app/reproducible-research/make.html).

When using the `GNU Make`, as can be seen in the Figure bellow, the Docker Compose interaction and possible configurations are performed by ready and tested code, avoiding several errors. Besides that, since it is a simple text document, the ones more interested in details, can open and verify the file.

<figure markdown>
  ![Examples flow](/assets/reproducible-research/minimal-example/examples-flow-make.svg){ width="1024" }
  <figcaption>Example flux with Make</figcaption>
</figure>

In the examples the `GNU Make` will be used alongside the `Makefile` to automatically make the configurations, to make the use of the materials simplier and more direct.

#### Makefile available commands

To facilitate the use of the `Makefile` commands, this subsectiion has a reference of each available command. These commands are divided in two groups: `Example` and `Replication`.

The `Example` commands facilitates the `Minimal example` operations, while `Replication` commands facilitates replication. Note that, both commands execute the same environments being the only change the input directory. So, if you wish to adapt the codes for your data, these commands can also be used. Alternatively, the Docker Compose used by the `Makefile` are also available and can be modified.

The following topics show the presented commands for each of these groups:

**Example**

<div align="center" markdown>
|       **Command**       |                            **Description**                                     |
|:-----------------------:|:------------------------------------------------------------------------------:|
| `example_cleanup_data`  | Removes all data (Input and output) used in the minimal example                |
| `example_download_data` | Downloads the data used by the minimal example                                 |
| `example_pipeline`      | Creates the Container to execute the minimal example through Dagster           |
| `example_notebook`      | Creates the Container to execute the minimal example through Jupyter Notebook  |
</div>

**Replication**

<div align="center" markdown>
|          **Command**         |                               **Description**                                     |
|:----------------------------:|:---------------------------------------------------------------------------------:|
| `replication_cleanup_data`   | Removes all data (Input and output) used in the replication                       |
| `replication_ download_data` | Downloads the data used by the replication                                        |
| `replication_pipeline`       | Creates the Container to execute the replication example through Dagster          |
| `replication_notebook`       | Creates the Container to execute the replication example through Jupyter Notebook |
</div>

As can be seen, the commands for both examples are the same, changing only the command call. As for their functionality, it is the same only changing the input data.

## requirements

Before starting the examples, ensure that you have the required tools configured in your work environment. Bellow, these tools are listed and described:

[Git](https://git-scm.com/)

:   Version control system (Documentation created with git version `2.25.1`. Posterior versions should support the used commands);

[Docker](https://www.docker.com/)

:   Virtualization software based on Containers (Documentation created using version `0.10.12`. Posterior versions should support the used commands);

[Docker Compose](https://docs.docker.com/compose/)

:   Orchestrator and manager tool for Docker Containers (Documentation created with Docker Compose versão `1.29.2`. Posterior versions should support the used commands)).

[GNU Make](https://www.gnu.org/software/make/)

:   Automatization and tool to control *build* flux and execution (Documentation created with `GNU Make` versão `4.2.1`. Posterior versions should support the used commands)).

Use the *links* above to access the official documentation of each tool and install them (case you don't have it installed).

!!! note "Operational System"

    The operational system used to create this RC materias was Ubuntu 20.04. It is expected that the presented steps work on similar or equivalent distributions (e.g., [MacOS](https://www.apple.com/br/macos/monterey/), [FreeBSD](https://www.freebsd.org/), [openSUSE](https://www.opensuse.org/)). Regarding Windows, adaptations may be required.

    If you use Windows and does not want to modify this RC, we also provided a virtual machine that can be used. For more information, please consult the Section [Computational Environments - Vagrant Virtual Machine](/en/tools/environment/#vagrant-virtual-machine).


After installing and configuring all the listed tools above, you are ready to start the examples.
