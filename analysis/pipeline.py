# -*- coding: utf-8 -*-

import os

from typing import List, Tuple
from dagster import pipeline, solid, OutputDefinition

import pipeline_utils


@solid(
   config_schema = {
    "landsat8_input_dir": str,
    "landsat8_sceneid_list": str,

    "sentinel2_input_dir": str,
    "sentinel2_sceneid_list": str,
    
    "derived_data_dir": str
  }, output_defs=[
      # Landsat-8
      OutputDefinition(name = "landsat8_input_dir"),
      OutputDefinition(name = "landsat8_sceneid_list"),
      
      # Sentinel-2
      OutputDefinition(name = "sentinel2_input_dir"),
      OutputDefinition(name = "sentinel2_sceneid_list"),
      
      # General
      OutputDefinition(name = "outdir_landsat8"),
      OutputDefinition(name = "outdir_sentinel2"),
  ])
def config_gatter(context) -> Tuple[Tuple[List, List], Tuple[List, List]]:
    """Configure and validate the input data before start pipeline"""
        
    #
    # Load Sentinel-2 scenes
    #
    with open(context.solid_config["sentinel2_sceneid_list"]) as file:
        scene_list = file.readlines()
        sentinel2_sceneids = pipeline_utils.standardize_filename(scene_list)
        
    #
    # Load Landsat-8 scenes
    #
    with open(context.solid_config["landsat8_sceneid_list"]) as file:
        scene_list = file.readlines()
        landsat8_sceneids = pipeline_utils.standardize_filename(scene_list)
        
    if len(landsat8_sceneids) != len(sentinel2_sceneids):
        raise RuntimeError("It is necessary to have the same amount of "
                               "landsat-8 and sentinel-2 scenes")
        
    # create base output directories (for each sensor)
    base_out_dir = context.solid_config["derived_data_dir"]
    
    s2_outputs = os.path.join(base_out_dir, "s2")
    lc8_outputs = os.path.join(base_out_dir, "lc8")
    
    return (
            context.solid_config["landsat8_input_dir"], 
            landsat8_sceneids,
            
            context.solid_config["sentinel2_input_dir"], 
            sentinel2_sceneids,
            
            lc8_outputs, 
            s2_outputs
        )


@solid(
 output_defs=[
      OutputDefinition(name = "sen2cor_sceneid"),
      OutputDefinition(name = "sen2cor_scene_path"),
])  
def apply_sen2cor(input_dir: str, output_dir: str, 
                      scene_ids: List) -> Tuple[List[str], List[str]]:
    
    from cfactor.surface_reflectance import sen2cor
    
    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "sen2cor_sr"    
    )

    sen2cor_scenes = sen2cor(input_dir, output_dir, scene_ids)
    sen2cor_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return (sen2cor_scene_ids, sen2cor_scenes)


@solid(config_schema = {    
    "auxiliary_data": str,
},  output_defs=[
      OutputDefinition(name = "lasrc_sceneid"),
      OutputDefinition(name = "lasrc_scene_path"),
])
def apply_lasrc(context, input_dir: str, output_dir: str, 
                scene_ids: List) -> Tuple[List[str], List[str]]:
    """
    """
    from cfactor.surface_reflectance import lasrc

    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "lasrc_sr"    
    )

    # select auxiliary data
    auxiliary_data = context.solid_config["auxiliary_data"]

    lasrc_scenes = lasrc(input_dir, output_dir, scene_ids, auxiliary_data)
    lasrc_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return (lasrc_scene_ids, lasrc_scenes)


@solid(output_defs=[
      OutputDefinition(name = "lc8_nbar_angles"),
])  
def lc8_nbar_angles(input_dir, scene_ids) -> List[str]:
    """
    """
    
    from cfactor.nbar import lc8_generate_angles

    return lc8_generate_angles(input_dir, scene_ids)


@solid(
 output_defs=[
      OutputDefinition(name = "lc8_nbar_sceneid"),
      OutputDefinition(name = "lc8_nbar_scene_path"),
])  
def lc8_nbar(input_dir: str, output_dir: str, scene_ids: List[str]): 
    """
    """
    
    from cfactor.nbar import lc8_nbar
    
    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "lc8_nbar"    
    )
    
    lc8_nbar_outdir = lc8_nbar(input_dir, output_dir, scene_ids)
    lc8_nbar_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return (lc8_nbar_scene_ids, lc8_nbar_outdir)


@pipeline
def cfactor_pipeline():
    
    #
    # Load and validate the input config
    #    
    (
      lc8_inputs, lc8_scenes, s2_inputs, s2_scenes, lc8_outputs, s2_outputs, 
    ) = config_gatter()
    
    #
    # Sentinel-2 Atmosphere correction (with sen2cor and LaSRC)
    #
    
    # sen2cor
    sen2cor_sceneids, sen2cor_scenes = apply_sen2cor(
        s2_inputs, s2_outputs, s2_scenes    
    )

    # LaSRC
    lasrc_sceneids, lasrc_scenes = apply_lasrc(
        s2_inputs, s2_outputs, s2_scenes    
    )
    
    #
    # Landsat-8 NBAR
    #
    scene_angles_lc8 = lc8_nbar_angles(lc8_inputs, lc8_scenes)
    
    lc8_nbar(lc8_inputs, lc8_outputs, scene_angles_lc8)
