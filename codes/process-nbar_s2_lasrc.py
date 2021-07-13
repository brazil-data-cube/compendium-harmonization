sceneids = [] # define an empty list

input_dir = '/harmonization/work/s2_sr_lasrc'
output_dir = '/harmonization/work/s2_nbar_lasrc'
s2_sceneids = '/harmonization/input/s2-sceneids.txt'

with open(s2_sceneids, 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

for sceneid in sceneids:
    print(f'docker run --rm -v {input_dir}:/mnt/input-dir:rw -v {output_dir}:/mnt/output-dir nbar {sceneid[:-5]}')
