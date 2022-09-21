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


# Reseach Compendium - Tools

The production and availability of this Research Compendium (RC) made it necessary that besides the code developed to produce the results of the article, we created additional scripts for the organization and publication of the research materials.

To make accessible and disseminate as many resources as possible, this directory contains all the extra tools that we used during the preparation of this RC. Listed below are the available tools:

- [calculate-checksum](calculate-checksum/): A tool for generating [BagIt](https://en.wikipedia.org/wiki/BagIt) from the data provided in this RC. It uses the features provided by the [bagit-python](https://libraryofcongress.github.io/bagit-python/) library as a base;

- [example-toolkit](example-toolkit/): Set of scripts with specific functionality for preparing the example environments available in this RC (Minimal example and Replication Example);

- [github-asset-upload](github-asset-upload/): Utility script for publishing BagIt to GitHub Release Assets. The script uses the R [piggyback package](https://cran.r-project.org/package=piggyback), which simplifies the data uploading to GitHub;

- [auxiliary-library](auxiliary-library): Python library with the main functionalities used to develop the processing scripts in this RC.
