import os
import shutil
from pathlib import Path

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

sceneids = [] # define an empty list
with open('/dados/Rennan/harmonization/input/s2-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

input_dir = '/dados/Rennan/harmonization/work/s2_sr_sen2cor'
output_dir = '/dados/Rennan/harmonization/work/s2_sr_lasrc'

for sceneid in sceneids:
    print(sceneid)

    l2aname = sceneid.replace('L1C','L2A')
    l2aname = l2aname.replace(l2aname.split('_')[3], 'N9999')
    pattern = '_'.join(l2aname.split('_')[:-1])
    l2a_dir = [d for d in os.listdir(input_dir) if d.startswith(pattern)][0]
    ang_dir = os.path.join(input_dir, l2a_dir, 'GRANULE', os.listdir(os.path.join(input_dir, l2a_dir, 'GRANULE'))[0], 'ANG_DATA')

    p_out = Path(output_dir).joinpath(sceneid.replace('.SAFE','')).joinpath('ANG_DATA')
    copy_and_overwrite(ang_dir, str(p_out))
