from datetime import datetime
from operator import itemgetter

sceneids = [] # define an empty list
with open('input/s2-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list
print(f'Total sceneids {len(sceneids)}')

s2_sceneids = []
for sceneid in sceneids:
    splited_sceneid = sceneid.split('_')
    sensing_date = datetime.strptime(splited_sceneid[2], '%Y%m%dT%H%M%S')
    orbit = int(splited_sceneid[4][1:])
    s2_sceneids.append([sceneid, sensing_date, orbit])

# Order by sensing_date
s2_sceneids = sorted(s2_sceneids, key=itemgetter(1))

day_diff = 5
pairs = []
uniques = set()
for i in range(0, len(s2_sceneids)-1):
    # Select with day difference
    if abs((s2_sceneids[i][1] - s2_sceneids[i+1][1]).days) < day_diff:
        # Select from other orbit
        if s2_sceneids[i][2] != s2_sceneids[i+1][2]:
            pairs.append((s2_sceneids[i][0], s2_sceneids[i+1][0]))
            uniques.add(s2_sceneids[i][0])
            uniques.add(s2_sceneids[i+1][0])


print(f'Total pairs: {len(pairs)}')
print(f'Total uniques: {len(uniques)}')

for pair in pairs:
    print(pair)
# for unique in uniques:
#     print(unique)
# print(uniques)

# print(f'Remove unused: {set(sceneids)-uniques}')