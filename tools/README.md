# Reseach Compendium - Tools

The production and availability of this Research Compendium (RC) made it necessary that besides the code developed to produce the results of the article, we created additional scripts for the organization and publication of the research materials.

To make accessible and disseminate as many resources as possible, this directory contains all the extra tools that we used during the preparation of this RC. Listed below are the available tools:

- [calculate-checksum](calculate-checksum/): A tool for generating [BagIt](https://en.wikipedia.org/wiki/BagIt) from the data provided in this RC. It uses the features provided by the [bagit-python](https://libraryofcongress.github.io/bagit-python/) library as a base;

- [example-toolkit](example-toolkit/): Set of scripts with specific functionality for preparing the example environments available in this RC (Minimal example and Replication Example);

- [github-asset-upload](github-asset-upload/): Utility script for publishing BagIt to GitHub Release Assets. The script uses the R [piggyback package](https://cran.r-project.org/package=piggyback), which simplifies the data uploading to GitHub;

- [auxiliary-library](auxiliary-library): Python library with the main functionalities used to develop the processing scripts in this RC.
