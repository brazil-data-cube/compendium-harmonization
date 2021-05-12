import json
import os

import rasterio
from rasterio.enums import Resampling
from rasterio.io import MemoryFile
from rasterio.transform import Affine
from rasterio.warp import reproject, calculate_default_transform
from rasterio.windows import Window
from shapely.geometry import box

import os

# 3rd party
from osgeo import gdal
import numpy


def raster_intersection(ds1, ds2, nodata1=None, nodata2=None, output_name1=None, output_name2=None):
    """Perform image intersection of two rasters with different extent and projection.
        Args:
            ds1 (GDAL dataset) - GDAL dataset of an image
            ds2 (GDAL dataset) - GDAL dataset of an image
            nodata1 (number) - nodata value of image 1
            nodata2 (number) - nodata value of image 2
            output_name1 (string) - path to output intersection of ds1
            output_name2 (string) - path to output intersection of ds2
        Returns:
            dataset1 (GDAL dataset), dataset2 (GDAL dataset): intersection dataset1 and intersection dataset2.
    """
    ###Setting nodata
    nodata = 0
    ###Check if images NoData is set
    if nodata2 is not None:
        nodata = nodata2
        ds2.GetRasterBand(1).SetNoDataValue(nodata)
    else:
        if ds2.GetRasterBand(1).GetNoDataValue() is None:
            ds2.GetRasterBand(1).SetNoDataValue(nodata)

    if nodata1 is not None:
        nodata = nodata1
        ds1.GetRasterBand(1).SetNoDataValue(nodata1)
    else:
        if ds1.GetRasterBand(1).GetNoDataValue() is None:
            ds1.GetRasterBand(1).SetNoDataValue(nodata)

    ### Get extent from ds1
    projection = ds1.GetProjectionRef()
    geoTransform = ds1.GetGeoTransform()

    ###Get minx and max y
    minx = geoTransform[0]
    maxy = geoTransform[3]

    ###Raster dimensions
    xsize = ds1.RasterXSize
    ysize = ds1.RasterYSize

    maxx = minx + geoTransform[1] * xsize
    miny = maxy + geoTransform[5] * ysize

    ###Warp to same spatial resolution
    gdaloptions = {'format': 'MEM', 'xRes': geoTransform[1], 'yRes': geoTransform[5], 'dstSRS': projection}
    ds2w = gdal.Warp('', ds2, **gdaloptions)
    ds2 = None

    ###Translate to same projection
    ds2c = gdal.Translate('', ds2w, format='MEM', projWin=[minx, maxy, maxx, miny], outputSRS=projection)
    ds2w = None
    ds1c = gdal.Translate('', ds1, format='MEM', projWin=[minx, maxy, maxx, miny], outputSRS=projection)
    ds1 = None

    ###Check if will create file on disk
    if output_name1 is not None or output_name2 is not None:
        driver = gdal.GetDriverByName("GTiff")
        if output_name1 is None:
            output_name1 = 'intersection1.tif'
        if output_name2 is None:
            output_name2 = 'intersection2.tif'
    else:
        driver = gdal.GetDriverByName("MEM")
        output_name1 = ''
        output_name2 = ''

    dataset1 = driver.Create(output_name1, xsize, ysize, 1, ds1c.GetRasterBand(1).DataType)
    dataset1.SetGeoTransform(geoTransform)
    dataset1.SetProjection(projection)
    dataset1.GetRasterBand(1).SetNoDataValue(nodata) ###Setting nodata value
    dataset1.GetRasterBand(1).WriteArray(ds1c.GetRasterBand(1).ReadAsArray())

    dataset2 = driver.Create(output_name2, xsize, ysize, 1, ds2c.GetRasterBand(1).DataType)
    dataset2.SetGeoTransform(geoTransform)
    dataset2.SetProjection(projection)
    dataset2.GetRasterBand(1).SetNoDataValue(nodata) ###Setting nodata value
    dataset2.GetRasterBand(1).WriteArray(ds2c.GetRasterBand(1).ReadAsArray())

    ds1c = None
    ds2c = None

    return dataset1, dataset2


#TODO Use Rasterio instead of GDAL
# def raster_intersection(raster1_path, raster2_path):
#     test_path='/home/marujo/Downloads/test.tif'
#     raster1 = rasterio.open(raster1_path)
#     raster2 = rasterio.open(raster2_path)

#     dst_crs = raster1.crs
#     src_crs = raster2.crs

#     print(raster2.shape)

#     # Check if data must be reprojected
#     if dst_crs != src_crs:
#         with rasterio.open(raster2_path) as src:
#             transform, width, height = calculate_default_transform(
#                 src.crs, dst_crs, src.width, src.height, *src.bounds)
#             kwargs = src.meta.copy()
#             kwargs.update({
#                 'crs': dst_crs,
#                 'transform': transform,
#                 'width': width,
#                 'height': height
#             })
#         with rasterio.open(test_path, 'w', **kwargs) as dst:
#             for i in range(1, src.count + 1):
#                 reproject(
#                     source=rasterio.band(src, i),
#                     destination=rasterio.band(dst, i),
#                     src_transform=src.transform,
#                     src_crs=src.crs,
#                     dst_transform=transform,
#                     dst_crs=dst_crs,
#                     resampling=Resampling.nearest)

#     raster2 = rasterio.open(test_path)

#     bb_raster1 = box(raster1.bounds[0], raster1.bounds[1], raster1.bounds[2], raster1.bounds[3])
#     bb_raster2 = box(raster2.bounds[0], raster2.bounds[1], raster2.bounds[2], raster2.bounds[3])

#     xminR1, yminR1, xmaxR1, ymaxR1 = raster1.bounds
#     xminR2, yminR2, xmaxR2, ymaxR2 = raster2.bounds

#     intersection = bb_raster1.intersection(bb_raster2)
#     transform = Affine(raster1.res[0], 0.0, intersection.bounds[0], 0.0, -raster1.res[1], intersection.bounds[3])

#     p1Y = intersection.bounds[3] - raster1.res[1]/2
#     p1X = intersection.bounds[0] + raster1.res[0]/2
#     p2Y = intersection.bounds[1] + raster1.res[1]/2
#     p2X = intersection.bounds[2] - raster1.res[0]/2
#     #row index raster1
#     row1R1 = int((ymaxR1 - p1Y)/raster1.res[1])
#     #row index raster2
#     row1R2 = int((ymaxR2 - p1Y)/raster2.res[1])
#     #column index raster1
#     col1R1 = int((p1X - xminR1)/raster1.res[0])
#     #column index raster2
#     col1R2 = int((p1X - xminR2)/raster1.res[0])

#     #row index raster1
#     row2R1 = int((ymaxR1 - p2Y)/raster1.res[1])
#     #row index raster2
#     row2R2 = int((ymaxR2 - p2Y)/raster2.res[1])
#     #column index raster1
#     col2R1 = int((p2X - xminR1)/raster1.res[0])
#     #column index raster2
#     col2R2 = int((p2X - xminR2)/raster1.res[0])

#     width1 = col2R1 - col1R1 + 1
#     width2 = col2R2 - col1R2 + 1
#     height1 = row2R1 - row1R1 + 1
#     height2 = row2R2 - row1R2 + 1

#     arr_raster1 = raster1.read(1, window=Window(col1R1, row1R1, width1, height1))
#     arr_raster2 = raster2.read(1, window=Window(col1R2, row1R2, width2, height2))

#     return arr_raster1, arr_raster2


def raster_absolute_diff(ds1, ds2, nodata1=None, nodata2=None, output_file=None):
    """Perform image absolute difference (support different extent and projection).
        Args:
            path1 (string) - path to image 1 (reference)
            path2 (string) - path to image 2 (target)
            output_dir (string) - path to output files
            nodata1 (number) - nodata value of image 1
            nodata2 (number) - nodata value of image 2
        Returns:
            dataset (GDAL dataset): dataset containing absolute difference between ds1 and ds2.
    """
    if output_file is None:
        output_file = 'abs_diff.tif'
    ds1_intersec, ds2_intersec = raster_intersection(ds1, ds2, nodata1, nodata2, None, None)

    ### Read bands with numpy to algebra
    nodata = ds1_intersec.GetRasterBand(1).GetNoDataValue()
    bandtar = numpy.array(ds1_intersec.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandtar = numpy.where(bandtar == nodata)
    bandref = numpy.array(ds2_intersec.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandref = numpy.where(bandref == nodata)

    ### Get extent from ds1
    projection = ds1.GetProjectionRef()
    geoTransform = ds1.GetGeoTransform()
    [cols, rows] = ds1.GetRasterBand(1).ReadAsArray().shape

    ds1 = None
    ds2 = None
    diff = numpy.abs(bandtar - bandref)
    diff[fill_bandtar] = nodata
    diff[fill_bandref] = nodata

    ###Check if will create file on disk
    if output_file is not None:
        driver = gdal.GetDriverByName("GTiff")
    else:
        driver = gdal.GetDriverByName("MEM")
        output_file = ''

    dataset = driver.Create(output_file, rows, cols, 1, ds1_intersec.GetRasterBand(1).DataType)
    dataset.SetGeoTransform(geoTransform)
    dataset.SetProjection(projection)
    dataset.GetRasterBand(1).SetNoDataValue(nodata)
    dataset.GetRasterBand(1).WriteArray(diff)

    return dataset

def raster_absolute_sum(ds1, ds2, nodata1=None, nodata2=None, output_file=None):
    """Perform image absolute difference (support different extent and projection).
        Args:
            path1 (string) - path to image 1 (reference)
            path2 (string) - path to image 2 (target)
            output_dir (string) - path to output files
            nodata1 (number) - nodata value of image 1
            nodata2 (number) - nodata value of image 2
        Returns:
            dataset (GDAL dataset): dataset containing absolute difference between ds1 and ds2.
    """
    if output_file is None:
        output_file = 'abs_diff.tif'
    ds1_intersec, ds2_intersec = raster_intersection(ds1, ds2, nodata1, nodata2, None, None)

    ### Read bands with numpy to algebra
    nodata = ds1_intersec.GetRasterBand(1).GetNoDataValue()
    bandtar = numpy.array(ds1_intersec.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandtar = numpy.where(bandtar == nodata)
    bandref = numpy.array(ds2_intersec.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandref = numpy.where(bandref == nodata)

    ### Get extent from ds1
    projection = ds1.GetProjectionRef()
    geoTransform = ds1.GetGeoTransform()
    [cols, rows] = ds1.GetRasterBand(1).ReadAsArray().shape

    ds1 = None
    ds2 = None
    raster_sum = bandtar + bandref
    raster_sum[fill_bandtar] = nodata
    raster_sum[fill_bandref] = nodata

    ###Check if will create file on disk
    if output_file is not None:
        driver = gdal.GetDriverByName("GTiff")
    else:
        driver = gdal.GetDriverByName("MEM")
        output_file = ''

    dataset = driver.Create(output_file, rows, cols, 1, ds1_intersec.GetRasterBand(1).DataType)
    dataset.SetGeoTransform(geoTransform)
    dataset.SetProjection(projection)
    dataset.GetRasterBand(1).SetNoDataValue(nodata)
    dataset.GetRasterBand(1).WriteArray(raster_sum)

    return dataset
###

from datetime import datetime
from operator import itemgetter

def search_pairs_l8(sceneids_file='input/l8-sceneids.txt'):
    sceneids = [] # define an empty list
    with open(sceneids_file, 'r') as filehandle: # open file and read the content in a list
        for line in filehandle:
            currentPlace = line[:-1] # remove linebreak which is the last character of the string
            sceneids.append(currentPlace) # add item to the list

    l8_sceneids = []
    for sceneid in sceneids:
        splited_sceneid = sceneid.split('_')
        sensing_date = datetime.strptime(splited_sceneid[3], '%Y%m%d')
        orbit = int(splited_sceneid[2])
        l8_sceneids.append([sceneid, sensing_date, orbit])

    # Order by sensing_date
    l8_sceneids = sorted(l8_sceneids, key=itemgetter(1))

    day_diff = 10
    pairs = []
    uniques = set()
    for i in range(0, len(l8_sceneids)-1):
        # Select with day difference
        if abs((l8_sceneids[i][1] - l8_sceneids[i+1][1]).days) < day_diff:
            # Select from other orbit
            if l8_sceneids[i][2] != l8_sceneids[i+1][2]:
                pairs.append((l8_sceneids[i][0], l8_sceneids[i+1][0]))
                uniques.add(l8_sceneids[i][0])
                uniques.add(l8_sceneids[i+1][0])

    return pairs
###


input_dir = '/home/marujo/Downloads/validation/l8_sr'
bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']

pairs = search_pairs_l8()
dif_dict = {}
relative_abs_perc_dict = {}
i=0
for b in bands:
    dif_dict[b] = []
    relative_abs_perc_dict[b] = []
    for pair in pairs:
        pair = ('LC08_L2SP_222081_20200723_20200910_02_T1','LC08_L2SP_223081_20200730_20200908_02_T1')
        print(f"Comparing band {b} pair {pair}")
        raster1_path = os.path.join(input_dir, pair[0]) + '/' + pair[0] + '_SR_' + b + '.TIF'
        raster2_path = os.path.join(input_dir, pair[1]) + '/' + pair[1] + '_SR_' + b + '.TIF'

        raster1 = gdal.Open(raster1_path)
        raster2 = gdal.Open(raster2_path)

        raster1_intersec, raster2_intersec = raster_intersection(raster1, raster2)
        raster1_band = raster1_intersec.GetRasterBand(1)
        raster2_band = raster1_intersec.GetRasterBand(1)
        raster1_arr = raster1_band.ReadAsArray().astype(float)
        raster2_arr = raster2_band.ReadAsArray().astype(float)
        
        # abs_dif = raster_absolute_diff(raster1, raster2)
        # dif_band = abs_dif.GetRasterBand(1)
        # dif_arr = dif_band.ReadAsArray()
        # dif_mean = dif_arr.mean()
        # dif_dict[b].append(dif_mean)

        # abs_sum = raster_absolute_sum(raster1, raster2)
        # sum_band = abs_sum.GetRasterBand(1)
        # sum_arr = sum_band.ReadAsArray()
        # relative_abs_perc = numpy.divide((2*dif_arr), sum_arr)
        # relative_abs_perc_mean = relative_abs_perc.mean()*100
        # relative_abs_perc_dict[b].append(relative_abs_perc_mean)



        i=i+1
        if i>=4:
            break

    dif_for_b = numpy.mean(dif_dict[b])
    print(dif_dict)
    print(bands)
    print(f'{b} band mean: {dif_for_b}')
    # break

with open('abs_reflec_dif.json', 'w') as file:
    file.write(json.dumps(dif_dict))

with open('relative_abs_perc.json', 'w') as file:
    file.write(json.dumps(relative_abs_perc_dict))