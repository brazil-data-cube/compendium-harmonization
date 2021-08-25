# Evaluating Landsat-8 and Sentinel-2 Nadir BRDF Adjusted Reflectance (NBAR) on South of Brazil through a Reproducible and Replicable environment

This repository is a Research Compendium of the article: "Evaluating Landsat-8 and Sentinel-2 Nadir BRDF Adjusted Reflectance (NBAR) on South of Brazil through a Reproducible and Replicable environment".

Input images: Lansat-8/OLI and Sentinel-2/MSI. Source: http://earthexplorer.usgs.gov/ and https://scihub.copernicus.eu/dhus/#/home.

Authors: Rennan de Freitas Bezerra Marujo (https://orcid.org/0000-0002-0082-9498), Felipe M. Carlos (0000-0002-3334-4315), Raphael W. Costa (), Carlos A. F. Noronha (), José Guilherme Fronza (https://orcid.org/0000-0002-0830-8101), Jeferson de Souza Arcanjo (), Anderson Soares (https://orcid.org/0000-0001-6513-2192), Gilberto R. Queiroz (https://orcid.org/0000-0001-7534-0219) and Karine R. Ferreira (https://orcid.org/0000-0003-2656-5504)

## 1. Environment Preparation
To replicate this article `docker` is required.

You can build the docker images (harmonization/environment/docker-files directory) or import them (harmonization/environment/docker-images directory);

### 1.1 Docker: Sen2cor
Load the image by:
`cd harmonization/environment/docker-images`

`docker load < sen2cor-fmask-2.9.0.tar.gz`

### 1.2 Docker: LaSRC LEDAPS Fmask
Load the image by:
`cd harmonization/environment/docker-images`

`docker load < lasrc_ledaps_fmask43.tar.gz`

### 1.3 Docker: Landsat Angle Bands
Load the image by:

`cd harmonization/environment/docker-images`

`docker load < l8angs.tar.gz`

### 1.4 Docker: NBAR
Load the image by:

`cd harmonization/environment/docker-images`

`docker load < nbar.tar.gz`

## 2. Input data preparation

### 2.1 Extract Sentinel-2 Data
`mkdir -p harmonization/work/s2/`

`for f in harmonization/input/data/s2_compressed/*.zip; do
    unzip $f -d harmonization/work/s2/
done`

### 2.2 Extract Landsat-8 Data
`mkdir -p harmonization/work/l8/`

`for f in harmonization/input/data/l8_compressed/*.tar; do
    tar xf $f --directory harmonization/work/l8 --one-top-level
done`


## 3. Process Surface Reflectance Data

The obtained Landsat-8 images are already surface reflectance products.
So let's process Sentinel-2 images.

### 3.1 Processing Sentinel-2 through Sen2cor 2.9.0 and Fmask 4.3
Open `process-sr_s2_sen2cor.py` and edit the paths.
After that, run `process-sr_s2_sen2cor.py` to obtain the running commands and execute them.

### 3.2 Processing Sentinel-2 through LaSRC 2.0.1 and Fmask 4.3
Download LaSRC auxiliary files (https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/)

Open `process-sr_s2_lasrc.py` and edit the paths.
After that, run `process-sr_s2_lasrc.py` to obtain the running commands and execute them.

## 4. Process NBAR
Now let's process the NBAR
### 4.1 Landsat-8 NBAR
#### 4.1.1 Generate Landsat Angle Bands
Open `generate-angle_l8.py` to edit the paths and execute it to obtain the running commands. After that, execute them.
#### 4.1.2 Processing Landsat-8 NBAR
Open `process-nbar_l8.py` to edit the paths and execute it to obtain the running commands. After that, execute them.

### 4.2 Sentinel-2 NBAR
### 4.2.1 Processing Sentinel-2 Sen2cor NBAR
Open `process-nbar_s2_sen2cor` to edit the paths and execute it to obtain the running commands. After that, execute them.
### 4.2.3 Copy Sentinel-2 Angle Bands to SR products folder
Open `copy-s2_angle-bands.py` to edit the paths and execute it.
### 4.2.4 Processing Sentinel-2 LaSRC NBAR
Open `process-nbar_s2_lasrc.py` to edit the paths and execute it to obtain the running commands and execute them.

## 5. Validation

### 5.1 L8 SR-NBAR Comparison
Open `validation-nbar_l8` to edit the paths and execute it.
### 5.2 S2 SR-NBAR Sen2cor Comparison
Open `validation-nbar_s2_sen2cor` to edit the paths and execute it.
### 5.3 S2 SR-NBAR LaSRC Comparison
Open `validation-nbar_s2_lasrc` to edit the paths and execute it.
### 5.4 L8 vs S2 SR Sen2cor Comparison
Open `validation-sr_l8_s2_sen2cor` to edit the paths and execute it.
### 5.5 L8 vs S2 SR LaSRC Comparison
Open `validation-sr_l8_s2_lasrc` to edit the paths and execute it.
### 5.6 L8 vs S2 NBAR Sen2cor Comparison
Open `validation-nbar_l8_s2_sen2cor` to edit the paths and execute it.
### 5.7 L8 vs S2 NBAR LaSRC Comparison
Open `validation-nbar_l8_s2_lasrc.py` to edit the paths and execute it.
## Citation

### Formated Citation

### Bibtex