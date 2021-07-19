#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from dagster import repository

from preprocessing.pipeline import cfactor_pipeline
from validation.pipeline import cfactor_validation_pipeline


@repository
def cfactor_pipeline_repository():
    return [
        cfactor_pipeline, cfactor_validation_pipeline
    ]
