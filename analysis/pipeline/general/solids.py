#
# This file is part of Brazil Data Cube compendium-harmonization.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""research-processing analysis general use solids."""

from dagster import solid, OutputDefinition
from dagster import Field, String, Tuple, List

from research_processing import toolbox


@solid(
    config_schema={
        "landsat8_sceneid_list": Field(
            config=String,
            description="path to a txt file that contains the ids that are to be processed. These ids must be "
                        "equivalent to the scene directory names that are contained in Landsat-8 data repository.",
        ),
        "sentinel2_sceneid_list": Field(
            config=String,
            description="path to a txt file that contains the ids that are to be processed. These ids must be "
                        "equivalent to the scene directory names that are contained in Sentinel-2 data repository.",
        )
    },
    output_defs=[
        # Landsat-8
        OutputDefinition(name="landsat8_sceneid_list",
                         dagster_type=List[String],
                         description="List with the name of the Landsat-8 scenes that should be used for processing."),

        # Sentinel-2
        OutputDefinition(name="sentinel2_sceneid_list",
                         dagster_type=List[String],
                         description="List with the name of the Sentinel-2 scenes that should be used for processing.")
    ],
    description="Load and standardize files with the scene ids that are to be used in the analysis pipeline. "
                "The defined scenes will be retrieved from the Landsat-8 and Sentinel-2 data directories. Scenes "
                "that do not have their scene ids mapped into the input files "
                "(`landsat8_sceneid_list` and `sentinel2_sceneid_list`) will not be processed."
)
def load_and_standardize_sceneids_input(context) -> Tuple[String, String]:
    """Load and Standardize Satellite Scene ids."""

    #
    # Load Landsat-8 scenes
    #
    with open(context.solid_config["landsat8_sceneid_list"]) as file:
        scene_list = file.readlines()
        landsat8_sceneids = toolbox.standardize_filename(scene_list)

    #
    # Load Sentinel-2 scenes
    #
    with open(context.solid_config["sentinel2_sceneid_list"]) as file:
        scene_list = file.readlines()
        sentinel2_sceneids = toolbox.standardize_filename(scene_list)

    return landsat8_sceneids, sentinel2_sceneids


__all__ = (
    "load_and_standardize_sceneids_input"
)
