import os

sceneids = [] # define an empty list
with open('input/l8-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

input_dir = '/dados/Rennan/harmonization/work/l8_sr'
output_dir = '/dados/Rennan/harmonization/work/l8_nbar'

for sceneid in sceneids:
    print(f'docker run --rm -v {os.path.join(input_dir, sceneid)}:/mnt/input-dir:rw -v {output_dir}:/mnt/output-dir:rw nbar {sceneid}')
