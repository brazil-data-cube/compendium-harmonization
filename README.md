# c-factor-article

This repository contains the scripts used to process and compare surface reflectance derived from The article: "X".

Input images: Lansat-8/OLI and Sentinel-2/MSI. Source: http://earthexplorer.usgs.gov/ and https://scihub.copernicus.eu/dhus/#/home.

Authors: Rennan de Freitas Bezerra Marujo (https://orcid.org/0000-0002-0082-9498), José Guilherme Fronza (https://orcid.org/0000-0002-0830-8101), Anderson Soares (https://orcid.org/0000-0001-6513-2192), Gilberto R. Queiroz (https://orcid.org/0000-0001-7534-0219) and Karine R. Ferreira (https://orcid.org/0000-0003-2656-5504)

## 1. Environment Preparation
To replicate this article `docker` is required.

You can build the docker images (harmonization/environment/docker-files directory) or import them (harmonization/environment/docker-images directory);

### 1.1 Docker: Sen2cor Fmask
Build the image by:
`cd harmonization/environment/docker-files/sen2cor-Fmask`
`docker build -t sen2cor-2.9.0_fmask-4.3 .`

or import it:
`docker load < sen2cor-2.9.0_fmask-4.3.tar.gz`
### 1.2 Docker: LaSRC LEDAPS Fmask
Build the image by:
`cd /dados/Rennan/harmonization/environment/docker-files/LaSRC-LEDAPS-Fmask`
`docker build -t lasrc_ledaps_fmask43 .`

or import it:
`docker load < lasrc_ledaps_fmask43.tar.gz`

### 1.3 Docker: Landsat Angle Bands
Build the image by:

`cd harmonization/environment/docker-files/landsat-angle-bands-docker`
`docker build -t l8angs .`

or import it:
`docker load < l8angs.tar.gz`
### 1.4 Docker: Sentinel-2 Angle Bands
Build the image by:

`cd harmonization/environment/docker-files/sentinel2-angle-bands-docker`
`docker build -t s2angs .`

or import it:
`docker load < s2angs.tar.gz`
### 1.5 Docker: NBAR
Build the image by:

`cd /dados/Rennan/harmonization/environment/docker-files/NBAR`
`docker build -t nbar .`

or import it:
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


## 3. Process Surface Reflectance Data and Cloud Mask

The obtained Landsat-8 images are already surface reflectance products.
So let's process Sentinel-2 images.
### 3.1 Processing Sentinel-2 through Sen2cor 2.9.0 and Fmask 4.3
run `process-sr_s2_sen2cor.py` to obtain the running commands and execute them

### 3.2 Processing Sentinel-2 through LaSRC 2.0.1 and Fmask 4.3
run `process-sr_s2_lasrc.py` to obtain the running commands and execute them

## 4. Process NBAR
Now let's process the NBAR
### 4.1 Landsat-8 NBAR
#### 4.1.1 Generate Landsat Angle Bands
run `generate-angle_l8.py` to obtain the running commands and execute them
#### 4.1.2 Processing Landsat-8 NBAR
run `process-nbar_l8.py` to obtain the running commands and execute them

### 4.2 Sentinel-2 NBAR
### 4.2.1 Processing Sentinel-2 Sen2cor NBAR
run `process-sr_s2_lasrc.py` to obtain the running commands and execute them
### 4.2.2 Generate Sentinel-2 Angle Bands
run `generate-angle_s2.py` to obtain the running commands and execute them
### 4.2.3 Copy Sentinel-2 Angle Bands to SR products folder
run `copy-s2_angle-bands.py` to copy the generated bands from the s2_toa folder to s2_sr_lasrc
### 4.2.4 Processing Sentinel-2 LaSRC NBAR
run `process-nbar_s2_lasrc.py` to obtain the running commands and execute them

## 5. Validation

### 5.1 L8 SR-NBAR Comparison

### 5.2 S2 SR-NBAR Sen2cor Comparison

### 5.3 S2 SR-NBAR LaSRC Comparison

### 5.4 L8 vs S2 SR Sen2cor Comparison

### 5.5 L8 vs S2 SR LaSRC Comparison

### 5.6 L8 vs S2 NBAR Sen2cor Comparison

### 5.7 L8 vs S2 NBAR LaSRC Comparison

## Citation

### Formated Citation

### Bibtex