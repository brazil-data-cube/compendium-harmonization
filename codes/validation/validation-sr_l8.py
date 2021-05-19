import os

# 3rd party
import numpy
import rasterio

import validation_funcs
import navigate

# Local
# input_dir = '/home/marujo/Downloads/validation/l8_sr'
# cloud_l8_dir = input_dir
# output_dir = '/tower/git_hub/marujore/c-factor-article/validation/l8_sr/'
# bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
# pairs = validation_funcs.search_pairs_l8('/tower/git_hub/marujore/c-factor-article/input/l8-sceneids.txt')
# pairs = [("LC08_L2SP_222081_20200723_20200910_02_T1", "LC08_L2SP_223081_20200730_20200908_02_T1")]

# # Datacube
input_dir = '/dados/Rennan/harmonization/work/l8_sr/'
cloud_l8_dir = input_dir
output_dir = '/dados/Rennan/harmonization/validation/l8_sr/'
bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
pairs = validation_funcs.search_pairs_l8('/dados/Rennan/harmonization/input/l8-sceneids.txt')


comparison_metrics = {}

for pair in pairs:
    comparison_metrics[pair[0]+'_x_'+pair[1]] = {}
    # Prepare Cloud Mask
    cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_l8_dir, pair[0]))
    cloud2_ds = rasterio.open(navigate.path_to_l8cloud(cloud_l8_dir, pair[1]))

    cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
    mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr, nodata=0)
    mask2 = validation_funcs.mask_pixel_bitwise(cloud2_arr, nodata=0)
    mask = numpy.logical_or(mask1, mask2) # Combined mask

    for b in bands:
        #Load files
        print(f"Comparing pair {pair} band {b}")
        raster1_ds = rasterio.open(navigate.path_to_l8srband(input_dir, pair[0], b))
        raster2_ds = rasterio.open(navigate.path_to_l8srband(input_dir, pair[1], b))

        # Get raster intersection
        raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)
        raster1_arr = raster1_arr.astype(float)
        raster2_arr = raster2_arr.astype(float)

        #Apply Cloud mask
        raster1_arr[mask] = numpy.nan
        raster2_arr[mask] = numpy.nan

        # Compare
        abs_dif = abs(raster1_arr - raster2_arr)
        abs_dif_mean = numpy.nanmean(abs_dif)
        abs_sum = abs(raster1_arr + raster2_arr)
        relative_abs_perc = numpy.divide((2*abs_dif), abs_sum, out=numpy.zeros_like(2*abs_dif), where=abs_sum!=0)
        relative_abs_perc_mean = numpy.nanmean(relative_abs_perc)*100

        # Store
        comparison_metrics[pair[0]+'_x_'+pair[1]][b] = {}
        comparison_metrics[pair[0]+'_x_'+pair[1]][b]['abs_dif_mean'] = abs_dif_mean
        comparison_metrics[pair[0]+'_x_'+pair[1]][b]['relative_abs_perc_mean'] = relative_abs_perc_mean

comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))
