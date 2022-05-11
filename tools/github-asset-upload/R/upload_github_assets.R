#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

library(magrittr)

#
# 1. Configuring GitHub
#
print("Configuring GitHub")

# GitHub Repository
github_repository <- Sys.getenv("GITHUB_REPOSITORY")

# GitHub Tag name
github_tagname <- Sys.getenv("GITHUB_TAGNAME")

#
# 2. Defining the data directories (Folder with the .zip files that should 
#    be uploaded to the repository)
#
print("Defining the data directories")

minimal_example_dir <- Sys.getenv("MINIMAL_EXAMPLE_DIRECTORY")
replication_example_dir <- Sys.getenv("REPLICATION_EXAMPLE_DIRECTORY")

#
# 3. Creating a new tag release
#
print("Creating a new tag release")

piggyback::pb_new_release(github_repository, github_tagname)

#
# 4. Uploading Minimal example files
#
print("Uploading Minimal example files")

list.files(minimal_example_dir) %>% lapply(function(file) {
  file_to_upload <- paste(minimal_example_dir, file, sep = "/")

  piggyback::pb_upload(file = file_to_upload, repo = github_repository, tag = github_tagname)
})

#
# 5. Uploading Replication example files
#
print("Uploading Replication example files")

list.files(replication_example_dir) %>% lapply(function(file) {
  file_to_upload <- paste(replication_example_dir, file, sep = "/")

  piggyback::pb_upload(file = file_to_upload, repo = github_repository, tag = github_tagname)
})
