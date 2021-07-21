#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os


def path_to_l8cloud(cloud_dir, sceneid):
    return os.path.join(os.path.join(cloud_dir, sceneid), sceneid+'_QA_PIXEL.TIF')


def path_to_l8srband(input_dir, sceneid, band):
    return os.path.join(os.path.join(input_dir, sceneid), sceneid+'_SR_'+band+'.TIF')


def path_to_l8nbarband(input_dir, sceneid, band):
    return os.path.join(os.path.join(input_dir, sceneid)+'_NBAR', sceneid+'_NBAR_'+band+'.tif')


def path_to_s2l2a_cloud(cloud_dir, sceneid):
    l2aname = sceneid.replace('L1C','L2A')
    l2aname = l2aname.replace(l2aname.split('_')[3], 'N9999')
    pattern = '_'.join(l2aname.split('_')[:-1])
    l2a_dir = [d for d in os.listdir(cloud_dir) if d.startswith(pattern)][0]
    img_dir = os.path.join(cloud_dir, l2a_dir, 'GRANULE', os.listdir(os.path.join(cloud_dir, l2a_dir, 'GRANULE'))[0], 'IMG_DATA')
    cloud2_file = sceneid.split('_')[5] + '_' + sceneid.split('_')[2] + '_SCL_20m.jp2'
    cloud2_path = os.path.join(img_dir, 'R20m', cloud2_file)

    return cloud2_path


def path_to_s2nbarlasrc_band(input_dir, sceneid, band):
    return os.path.join(input_dir, sceneid.replace('.SAFE','')+'_NBAR', sceneid.replace('.SAFE','')+'_'+band+'.tif')


def path_to_s2nbarsen2cor_band(input_dir, sceneid, band):
    bands10m = ['B02', 'B03', 'B04', 'B08']
    bands20m = ['B8A', 'B11', 'B12']
    if band in bands20m:
        res = 20
    elif band in bands10m:
        res = 10
    raster_file = '_'.join([sceneid.split('_')[5], sceneid.split('_')[2], band, str(res)+'m.tif'])
    l2aname = sceneid.replace('L1C','L2A')
    l2aname = l2aname.replace(l2aname.split('_')[3], 'N9999')
    pattern = '_'.join(l2aname.split('_')[:-1])
    l2a_dir = [d for d in os.listdir(input_dir) if d.startswith(pattern)][0]
    img_dir = os.path.join(input_dir, l2a_dir)
    return os.path.join(img_dir, raster_file), res


def path_to_s2srlasrc_band(input_dir, sceneid, band):
    return os.path.join(input_dir, sceneid.replace('.SAFE',''), sceneid.replace('.SAFE','')+'_'+band+'.tif')


def path_to_s2srsen2cor_band(input_dir, sceneid, band):
    bands10m = ['B02', 'B03', 'B04', 'B08']
    bands20m = ['B8A', 'B11', 'B12']
    if band in bands20m:
        res = 20
    elif band in bands10m:
        res = 10
    raster_file = '_'.join([sceneid.split('_')[5], sceneid.split('_')[2], band, str(res)+'m.jp2'])
    l2aname = sceneid.replace('L1C','L2A')
    l2aname = l2aname.replace(l2aname.split('_')[3], 'N9999')
    pattern = '_'.join(l2aname.split('_')[:-1])
    l2a_dir = [d for d in os.listdir(input_dir) if d.startswith(pattern)][0]
    img_dir = os.path.join(input_dir, l2a_dir, 'GRANULE', os.listdir(os.path.join(input_dir, l2a_dir, 'GRANULE'))[0], 'IMG_DATA')
    return os.path.join(img_dir, 'R'+str(res)+'m', raster_file), res
