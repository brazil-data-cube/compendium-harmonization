<!--
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
-->


*[RC]: Research Compendium

# Replicação example

!!! attention "requirements"

    Before starting this example, verify if all the [requirements](/en/reproducible-research/#requirements) are installed in your work environment.

!!! attention "Base experiment"

    This is an example that uses the RC materials to process data from a region that isn't considered in the original article. The objective is to show that the tool has characteristics that makes it reproducible and replicable.

    If you haven't performed the first example ([Minimal exemple](/en/reproducible-research/minimal-example/)), it is recommended to do it before starting this one.


## Download the Research Compendium

To execute this example first you should *download* this RC and its materials. To do that, in a terminal, use `git` to [clone](https://git-scm.com/docs/git-clone) the repository in which this RC is stored:

``` sh
git clone https://github.com/brazil-data-cube/compendium-harmonization
```

After the [clone](https://git-scm.com/docs/git-clone), a new directory will be created in your current directory. The name of this new directory is `compendium-harmonization`:

``` sh
ls -ls .

#> 4 drwxrwxr-x 3 ubuntu ubuntu 4096 May  2 00:44 compendium-harmonization
```

Now, access the directory `compendium-harmonization` and list its content:

*Changing directory*
``` sh
cd compendium-harmonization
```

*Listing directory content*

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

As you can see, the content of the directory represents all the materials found on this RC. This will be the content used to execute this tutorial.

## Data Download

To *download* the replication example data you can use the following command:

``` sh
make replication_ download_data
```

Verify if the data were downloaded at the directory `analysis/data/examples/replication_example/`. It must be similar to the following:

```
.
├── landsat8_data
├── lasrc_auxiliary_data
├── scene_id_list
└── sentinel2_data
```

## Data Processing

The data processing can be performed through `Jupyter Notebook` or `Dagster`.

For each approach, automatic commands can be used through the `Makefile`. You can check bellow how to start it from each of the environments:

*Jupyter Notebook*

``` sh
make replication_notebook
```

!!! attention "Changes required"

    As the replication example uses other data from that presented in the minimal example, you should modify some Jupyter Notebook parameters — specifically, the `day_diff` parameter. This parameter defines the number of days difference between images. This change should only be made for tests where only Sentinel-2 is used.
    
    So, you must change the following sections of the Jupyter Notebook:

    - `4.3.1: Searching for image pairs`
    - `4.4.1: Searching for image pairs`
    - `4.5.1: Searching for image pairs`
    - `4.6.1: Searching for image pairs`

    In all of them, you must change `day_diff` to `15 days`:

    ```python
    validation_funcs.search_pairs_s2(sentinel2_sceneid_list, day_diff=15)
    ```

*Dagster*

``` sh
make replication_pipeline
```

!!! attention "Changes required"

    As the replication example uses other data from that presented in the minimal example, you should modify some Jupyter Notebook parameters — specifically, the `day_diff` parameter. This parameter defines the number of days difference between images. This change should only be made for tests where only Sentinel-2 is used.
    
    So, you must add the following changes to the `solids` section of your [Dagster configuration file](/en/tools/utilitary):

    ```yaml
    solids:
        validation_sr_s2_sen2cor:
            config:
            day_difference: 15
        validation_sr_s2_lasrc:
            config:
            day_difference: 15
        validation_nbar_s2_sen2cor:
            config:
            day_difference: 15
        validation_nbar_s2_lasrc:
            config:
            day_difference: 15
    ```

Once the environment is chosen, the processing and data analysis can be performed.
