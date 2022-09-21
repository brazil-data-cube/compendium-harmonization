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
*[SAA]: Solar Azimutal
*[SZA]: Solar Zenital
*[VAA]: Sensor Azimutal
*[VZA]: Sensor Zenital

# Software Libraries

Reproducibility allows us to retrace the path that was initially taken to obtain the results of scientific research. With this, other researchers and even our future selves can benefit and understand what we have done. The reproducibility also enables us to detect and correct possible errors in the results.

Among the many actions that can be taken to achieve reproducibility is the ability to automate the steps already performed. This brings several benefits:

1. Avoids possible "mistakes" by reading incorrect results that are no longer valid for the current run;
2. It allows the verification of the entire processing flow (which also helps in the writing of the report/article);
3. Decreased overhead of running the job.

A few years ago, this feature was limited in research due to the use of software with graphical interfaces that ended up not allowing the automation of the work done through "buttons and clicks" on the screen.

Nowadays, with the increase and dissemination of high-level languages for research development, such as [R](https://www.r-project.org/) and [Python](https://www.python.org/), this has completely changed. We can automate tasks more efficiently. Also, from the moment a processing script is created, all the logic applied to the data is described clearly and directly.

In this RC, several Python code libraries were created so that all steps could be modeled through scripts. Each library created has a unique responsibility, which helped us keep the work organized during its development. At the same time, this approach facilitates the reuse of the code created. Those who wish to reuse the work developed can import these libraries into their Python project.

## Available code libraries

To adopt this development approach, based on single responsibility libraries that could be reused, it was necessary to adopt some criteria that would help us keep everything organized and reusable. Also, our vision for creating multiple libraries for the composition of the scripts for processing the work is that these should be modeled in a way that they can be used together. Like blocks that can be put together to build a wall. 

Considering these characteristics, initially, we defined that in this RC, we would develop two types of libraries:

`Base`

:   Libraries that provide the base features and functionality for performing an action
    (e.g., Production of angle bands)

`Application`

:   Libraries that, through the union of **Base** libraries, provide functionalities that different methodologies and processing flows (e.g., Generation of harmonized products).

Based on these definitions, for the production of this RC and the generation of its results, we developed two **Base** libraries:

[s2-angs](https://github.com/brazil-data-cube/s2-angs)

:   Library create to provide functionality for generating angle bands from Sentinel-2/MSI data;


[sensor-harm](https://github.com/brazil-data-cube/sensor-harm)

:   Library create to generate harmonized produts from Sentinel-2/MSI and Landsat-8/OLI data;

These libraries are available and can be installed like any other Python language library and used in different projects. So, if you are interested, you can, for example, install the `sensor-harm` library in your Python project and utilize the functionality provided for generating harmonized products. For both libraries, the only restriction is to respect the input formats expected by the library functions. If followed correctly, you should have no problem using them.

Based on these two libraries, we created an **Application** library:

[research-processing](#)

:   Library created to provide functionality that allows the application of the data processing methodology used to generate the results of this RC. Part of its functionality is built upon the `s2-angs` and `sensor-harm` libraries.

The relationship between these libraries is summarized in the Figure below.

<figure markdown>
  ![Libraries organization](/assets/tools/libraries/libraries-organization/libraries-organization.svg){ width="1024" }
  <figcaption>Libraries organization</figcaption>
</figure>

Details of the operation and functionality of each of these libraries are presented in the following sections.

## Libraries in the processing methodology

The figure below gives you an overview of where the libraries presented above are used in the processing methodology:

<figure markdown>
  ![Processing workflow with libraries](/assets/tools/libraries/experiment-diagram/experiment-diagram.svg){ width="1024" }
  <figcaption>Processing workflow with libraries</figcaption>
</figure>

## Libraries specification

In this section, as a complement to the overview presented so far, the `features` and `usage example` of each of the aforementioned libraries are specified.

### Sentinel-2 Angle Generator Python Library (s2-angs)
[![s2-angs-badge-stars](https://img.shields.io/github/stars/brazil-data-cube/s2-angs?style=social)](https://github.com/brazil-data-cube/s2-angs)
[![s2-angs-badge-forks](https://img.shields.io/github/forks/brazil-data-cube/s2-angs?style=social)](https://github.com/brazil-data-cube/s2-angs)
[![s2-angs-badge-version](https://img.shields.io/github/v/release/brazil-data-cube/s2-angs?style=social)](https://github.com/brazil-data-cube/s2-angs)

The [s2-angs](https://github.com/brazil-data-cube/s2-angs) library, as mentioned earlier, is responsible for generating angle bands for Sentinel-2 imagery. These bands contain per-pixel information for solar azimuthal (SAA), solar zenithal (SZA), azimuthal sensor (VAA), and zenithal sensor (VZA) angles. This information is extracted from the Sentinel-2 image metadata. Initially, this data is provided as a `23x23` (rows X columns) matrix, i.e., at a spatial resolution of about `5000` meters. However, this information needs to be at a spatial resolution equivalent to that of the spectral bands of the sensor (`10`, `20` or `60` meters) to take advantage of per-pixel corrections. Thus, the s2-angs library can estimate angles and save them as `.tif` files, either at their original spatial resolution or resampled to the spatial resolution of the sensor bands.

So, we can list as main features of this library:

- Generation of angle bands ( `SAA`, `SZA`, `VAA` and `VZA` );
- Resampling the angle bands to the sensor band resolution.

#### Operations available

The table below gives a summary of the operations that are available in the [s2-angs](https://github.com/brazil-data-cube/s2-angs) library.

<div align="center" markdown>
|     **Function**      |                 **Description**                 |
|:---------------------:|:-----------------------------------------------:|
| `s2_angs.gen_s2_ang`  | Function to generate the Sentinel-2 Angle bands |
</div>

#### Usage example

Using the `s2_angs` library, use the `gen_s2_ang` function to perform angle band generation. This function accepts as input `.zip`, `.SAFE directory` or `directory with Sentinel-2 images`. In the code block below is an example where a `.zip` file is used as input to the function:

```py linenums="1" title="s2-angs example code"
import s2_angs

s2_angs.gen_s2_ang(
  "S2B_MSIL1C_20191223T131239_N0208_R138_T23KMR_20191223T135458.zip"
)
```

The above code will generate the angle bands from the image defined in the input. Examples of the results can be seen in the figures below:

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

To learn more about the library, please, see the [official s2-angs library repository](https://github.com/brazil-data-cube/s2-angs) on GitHub.

## Sensor Harmonization Python Library (sensor-harm)
[![s2-angs-badge-stars](https://img.shields.io/github/stars/brazil-data-cube/sensor-harm?style=social)](https://github.com/brazil-data-cube/sensor-harm)
[![sensor-harm-badge-forks](https://img.shields.io/github/forks/brazil-data-cube/sensor-harm?style=social)](https://github.com/brazil-data-cube/sensor-harm)
[![sensor-harm-badge-version](https://img.shields.io/github/v/release/brazil-data-cube/sensor-harm?style=social)](https://github.com/brazil-data-cube/sensor-harm)

In this RC, part of the results consists of harmonized products, i.e., surface reflectance level products with correction for `Bi-Directional Reflectance Distribution Function` (BRDF) effects and spectral adjustments. For this purpose, the [sensor-harm](https://github.com/brazil-data-center/sensor-harm) library was created. The BRDF correction is done using the `c-factor` method to generate Nadir BRDF-Adjusted Reflectance (NBAR) products in this library. In contrast, the spectral adjustment is made using `bandpass` adopting Landsat-8 images as the reference. Using this library, these methods can be applied to images from Landsat-4/TM, Landsat-5/TM, Landsat-7/ETM+, Landsat-8/OLI, and Sentinel-2/MSI sensor satellites. They can be harmonized between these different data. The library features two main functions, one for harmonizing images from sensors onboard the Landsat satellites and one for images from sensors onboard the Sentinel-2 satellites.

#### Operations available

The table below summarizes the operations available in the [sensor-harm](https://github.com/brazil-data-cube/sensor-harm) library.

<div align="center" markdown>
|     **Function**                           |                 **Description**                 |
|:------------------------------------------:|:-----------------------------------------------:|
| `sensor_harm.landsat.landsat_harmonize`    |       Function to harmonize Landsat data        |
| `sensor_harm.sentinel2.sentinel_harmonize` |       Function to harmonize Sentinel-2 data     |
</div>

#### Usage example

To perform data harmonization, be it Landsat-4/TM, Landsat-5/TM, Landsat-7/ETM+, Landsat-8/OLI, or Sentinel-2, it is necessary to define the directory where the input data is stored, as well as the output directory. To exemplify the use of this function, the code block below is an example of how we can use the `sensor-harm` library for Sentinel-2 data harmonization:

```py linenums="1" title="sensor-harm example code"
from sensor_harm.sentinel2 import sentinel_harmonize

sentinel2_entry = '/path/to/S2/SR/images/'
target_dir = '/path/to/output/NBAR/'

sentinel_harmonize(sentinel2_entry, target_dir, apply_bandpass=True)
```

The above code will generate the angle bands from the image defined in the input. Examples of the results can be seen in the figures below:

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

To learn more about the library, please, see the [official sensor-harm library repository](https://github.com/brazil-data-cube/sensor-harm) on GitHub.

## Research Processing Python Library (research-processing)

As presented in the previous sections, the processing methodology performed in this RC has several steps, which depend on different software tools. Consequently, the completion of the entire processing flow may require:

1. installation of specific software dependencies for each processing step;
2. Specific configurations in the software environment for each processing step.

With these requirements, the execution and reproduction of the processing flow could be problematic for us, and those who wish to reproduce or even apply the work developed. To avoid these possible problems and facilitate the materialization of this RC processing methodology, we developed the `research-processing` library. In this library, all the methodology steps are modeled as Python functions that can be easily used to build any processing flow. Additionally, part of the operations that require environment-specific configurations is executed in `Docker Containers`, transparently to the users of the library. All in all, you have `research-processing`, functionalities for performing actions such as:

**Preprocessing**

- Sentinel-2/MSI atmospheric correction (Sen2Cor and LaSRC);
- Angle band generation (Landsat-8/OLI and Sentinel-2/MSI);
- Generation of NBAR products (Sentinel-2/MSI and Landsat-8/OLI).

**Data analysis**

- Routines for validating the products created in the processing flow.

### Function Execution Approach

As mentioned earlier, the `research-processing` features are modeled as reusable functions with play-friendly execution. To ensure that these characteristics could be guaranteed, we adopted the `execution model` concept. This concept determines where/how the function will be executed transparently to the user. Each of the functions implemented in the library has an `execution model`, allowing different technologies and approaches to be used as a basis to execute the function. Based on the needs of the RC functions, two `execution models' were used in the implementations, namely:

`Local`

:   Functions implemented with the `Local` execution model are simple Python functions. These functions do not have any particular execution format and are executed directly in the environment/interpreter that invokes them. Functions with this format depending on the surrounding environment, which requires all dependencies to be installed and properly configured.

`Containerized`

:   Unlike `Local` functions, `Containerized` functions do not depend on the surrounding environment. This is because functions implemented with this format, when executed, create a `Docker Container`, with the complete environment necessary for the execution of the operation associated with the function. The function is executed within the created environment.

Both execution models are transparent to the user at runtime. So regardless of how the implementation was done, in the end, for the users, we have a call to a Python function. The difference lies in the demands that each type of function will make on the environment where it is being executed. As mentioned, for `Local` functions, you will need to install all the dependencies and settings to run the function. Meanwhile, `Containerized` functions will require Docker to be available in the user's environment.

!!! info "Containerized - User Permissions"

    It is important to note that besides having Docker installed, it is also necessary for the user who is running it to have the appropriate permissions to use Docker. 

The figure below is a general representation of each of these models used. Note that `Local` functions work with the Python interpreter, while `Containerized` functions create `Docker Containers` where execution will take place.

<figure markdown>
  ![Libraries organization](/assets/tools/libraries/research-processing/execution-model/execution-model-example.svg){ width="1024" }
  <figcaption>Research Processing Execution Models</figcaption>
</figure>

Based on these two modes of operation, the library implements and provides `processing` and `analysis` operations on the data. The `Containerized` mode of operation is used for processing operations, which use third-party tools like **Sen2Cor** and **LaSRC**. The `Local` mode of operation is used for validation operations, which uses only Python libraries as dependencies.

#### Function communication approach

The `research-processing` library features can be used together to build a processing flow that allows the materialization of the experiment methodology followed in this RC. In this context, one point to consider is how the inputs and outputs of these functions are used together. 

In `research-processing`, the implemented operations are performed in a way that avoids data movement (Inputs and Outputs). To do this, the processing functions operate based on the `data path`. This gives the functions the path where the data is stored and where the results should be saved. This mode of operation allows better definitions regarding where the data will be loaded and saved, avoiding unnecessary movement and storage in places that can present problems with space limitation and inadequate performance. This mode of operation is represented in the figure below.

<figure markdown>
  ![Libraries organization](/assets/tools/libraries/research-processing/data-flow/data-flow.svg){ width="1024" }
  <figcaption>Function communication model</figcaption>
</figure>

Based on this mode of operation, functions are chained together. The outputs of one function, representing the path to where the data was saved, are used as input in other functions.

!!! info "Inputs as volumes"

    For the `Containerized` functions, you should note that this data path information is used for creating [Docker Bind Mount Volumes](https://docs.docker.com/storage/volumes/). Thus, the auxiliary Containers process, created by the research-processing library, has access to the processed data.

!!! caution "Order of Operation"

    With this input/output format of functions, it is assumed that the output of one function will be understood by the following function. Thus, the functions available in the `research-processing` library must be chained together in a strict order, in this case, the order described in the methodology.

    For more details on how this can be implemented, see the section [Processing scripts](/en/tools/processing/).


### Operations available

To support the creation of the entire operation flow implemented in this RC, the `research-processing` library provides several auxiliary functions and operations, which are listed in the table below:


|                      **Function**                    |                                          **Description**                                      | **Execution model**    |
|:----------------------------------------------------:|:---------------------------------------------------------------------------------------------:|:----------------------:|
|   `research_processing.surface_reflectance.sen2cor`  |                        Sen2Cor Atmospheric Correction for Sentinel-2/MSI                        |      Containerized     |
|    `research_processing.surface_reflectance.lasrc`   |                         LaSRC Atmospheric Correction for Sentinel-2/MSI                        |      Containerized     |
|      `research_processing.nbar.s2_sen2cor_nbar`      | NBAR product generator for Sentinel-2/MSI surface reflectance data (Sen2Cor)              |      Containerized     |
|       `research_processing.nbar.s2_lasrc_nbar`       |   NBAR product generator for Sentinel-2/MSI surface reflectance data (LaSRC)  |      Containerized     |
|          `research_processing.nbar.lc8_nbar`         |         NBAR product generator for Landsat-8/OLI surface reflectance data        |      Containerized     |
|    `research_processing.nbar.lc8_generate_angles`    |                          Angle Generator for Landsat-8/OLI data                          |      Containerized     |
| `research_processing.validation.validation_routines` |                     Results Analysis (Module with multiple functions)                     |          Local         |

Among these functions, some details need to be considered to fully understand the rationale behind each of the `execution models` chosen for the functions. In the subtopics below, these details are presented:

**Sentinel-2/MSI atmospheric correction (Sen2Cor and LaSRC)**

The processing flow requires that the images used have an atmospheric correction. For Landsat-8/OLI images, there is no need to correct since the products are already available ready for use, with the proper geometric and radiometric corrections performed. However, for Sentinel-2/MSI data, this is not true. Thus, during the development of the article, it was necessary to perform the atmospheric correction of these data. For this, we adopted the tools [Sen2Cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/) and [LaSRC](https://ntrs.nasa.gov/api/citations/20190001670/downloads/20190001670.pdf).

These tools have their specific needs in the environment where they will be used, like dependencies and configurations. In the `research-processing` library, we created functions that operate these tools in an environment already configured and ready to use. This environment runs in a `Docker Container`.

From the functions presented in the table above, the ones listed below are used to apply atmospheric correction to the data:

- `research_processing.surface_reflectance.lasrc`: Function that applies Atmospheric Correction to Sentinel-2/MSI data using the LaSRC tool. All processing is performed inside a `Docker Container` transparently to the user;
- `research_processing.surface_reflectance.sen2cor`: Function that applies Atmospheric Correction to Sentinel-2/MSI data using the Sen2Cor tool. All processing is done inside a `Docker Container` transparently to the user.

!!! info "Understanding the Containers"

    Creating a `Docker Container` depends on a `Docker Image` that defines the environment and its settings. This is no different in `research-processing`. For the creation of Atmospheric Correction `Docker Containers`, the following `Docker Images` are used:

      - Atmospheric correction with LaSRC: [LaSRC 2.0.1 Docker Image](/environment/#lasrc-201)
      - Atmospheric correction with Sen2Cor: [Sen2Cor 2.9.0 Docker Image](/pt/tools/environment/#sen2cor-290)

    These `Docker Images` were created to run in this RC. For more information, see the [Computational Environments](/en/tools/environment) section.

**Angle band generation (Landsat-8/OLI and Sentinel-2/MSI)**

To generate NBAR products, angle bands (e.g., SAA, SZA, VAA, and VZA) must be calculated. These bands are explicitly developed for each data/sensor being worked on. This requires the use of specialized tools for each sensor:

- Landsat-8/OLI: The generation of angle bands for Landsat-8/OLI is done using the [Landsat 8 Angles Creation Tools](https://www.usgs.gov/media/files/landsat-8-angles-creation-tools-readme) tool. This tool has its own dependencies and also requires specific settings in the environment where it will be run;

- Sentinel-2/MSI: The angles from Sentinel-2/MSI data are generated with the [Sentinel-2 Angle Generator Python Library (s2-angs)](/en/tools/libraries/#sentinel-2-angle-generator-python-library-s2-angs) library, developed in this RC.

Considering these characteristics, you have the following function to perform these operations:

`research_processing.nbar.lc8_generate_angles`: A Function uses the [Landsat 8 Angles Creation Tools](https://www.usgs.gov/media/files/landsat-8-angles-creation-tools-readme) tool to perform the calculation of angle bands for Landsat-8/OLI data. The processing performed by this function is done inside a `Docker Container`.

In the above list of functions, there is no function specific to Sentinel-2/MSI. During the `research-processing` library implementation, we decided that the generation of angles for Sentinel-2/MSI data would be an integrated operation with the generation of NBAR products. Thus, the calculation of the angles required for the generation of NBAR products with Sentinel-2/MSI data, done with the s2-angs library, are part of the following functions:

  - `research_processing.nbar.s2_sen2cor_nbar`
  - `research_processing.nbar.s2_lasrc_nbar`

The processing performed by both functions listed above is also done inside a `Docker Container`.

!!! info "Understanding the Containers"

    Creating a `Docker Container` depends on a `Docker Image` that defines the environment and its settings. This is no different in `research-processing`. To create the `Docker Container` angle band generation, the following `Docker Image` is used:

      - Angle band generation for Landsat-8/OLI data: [L8Angs Docker Image](/pt/tools/environment/#l8angs)

    The `L8Angs Docker Image` was created to run in this RC. For more information, see the [Computational Environments](/en/tools/environment) section.

**NBAR products generation (Sentinel-2/MSI and Landsat-8/OLI)**

The basis for generating NBAR products in this RC, as presented in the previous sections, is the `sensor-harm` library. This library allows the generation of NBAR products for Sentinel-2/MSI and Landsat-8/OLI data. As a way to facilitate the use of the `sensor-harm` library and to avoid users having to do specific installations and configurations, in the `research-processing` library, the implementation of the following functions was performed:

- `research_processing.nbar.lc8_nbar`: A function to generate NBAR products for Landsat-8/OLI data;
- `research_processing.nbar.s2_lasrc_nbar`: A function to generate NBAR products for Sentinel-2/MSI data with the atmospheric correction made with the LaSRC tool;
- `research_processing.nbar.s2_sen2cor_nbar`: A function to generate NBAR products for Sentinel-2/MSI data with the atmospheric correction made with the Sen2Cor tool;

These functions are implemented with the `execution model` Containerized. Thus, when the user executes these functions, a `Docker Container` with the appropriate dependencies is created to perform the function.

!!! info "Understanding the Containers"

    Creating a `Docker Container` depends on a `Docker Image` that defines the environment and its settings. This is no different in `research-processing`. To create the NBAR product generation `Docker Container` (all functions), the following `Docker Image` is used:

      - NBAR product generation (Sentinel-2/MSI e Landsat-8/OLI): [NBAR Docker Image](/pt/tools/environment/#nbar)

    The `NBAR Docker Image` was created to run in this RC. For more information, see the [Computational Environments](/en/tools/environment) section.

**Routines for validating the products created in the processing flow**

There is the corrections validation module to evaluate the products generated with the processing flow. This module (`research_processing.validation.validation_routines`), is responsible for all the comparisons and calculations used to evaluate the results generated in this RC. It is implemented with the Local `execution model` to make debugging more straightforward. Thus, the user, who uses the functions of this module, must configure the environment where the execution will be performed. In short, one only has to install the `research-processing` library's dependencies. Then the environment is ready to execute these functions.

### Usage example

To exemplify how the `research-processing' library is used, below is how the library performs atmospheric correction of Sentinel-2/MSI images, using the [Sen2Cor](https://step.esa.int/main/snap-supported-plugins/sen2cor/) tool.

**Atmospheric correction Sen2Cor**

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

The above code will generate images with atmospheric correction. Examples of results can be seen in the figures below:

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
