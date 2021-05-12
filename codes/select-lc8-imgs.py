import glob
import os


def adapt_to_json(mtl_content: list) -> dict:
    output = dict()

    last_group = None

    for line in mtl_content:
        # line = line.strip()
        line_fragments = line.split(' = ')

        if len(line_fragments) != 2:
            continue

        key, value = line_fragments
        value = value.strip()

        if key.strip() == 'GROUP':
            last_group = value
            output.setdefault(value, dict())
        else:
            output[last_group][key.strip()] = value.replace('"', '')

    output.pop('LANDSAT_METADATA_FILE', None)
    return dict(LANDSAT_METADATA_FILE=output)

path = '/tower/Exp_Harmonization/l8-ang-mtl'
mtl_files = glob.glob(os.path.join(path, '*MTL.txt'))

cloud_scenes = []
for mtl in mtl_files:
    with open(mtl) as f:
        j = adapt_to_json(f.readlines())
        if(float(j['LANDSAT_METADATA_FILE']['IMAGE_ATTRIBUTES']['CLOUD_COVER'])) > 50.:
            # print(f"Remove {j['LANDSAT_METADATA_FILE']['PRODUCT_CONTENTS']['LANDSAT_PRODUCT_ID']} that has {j['LANDSAT_METADATA_FILE']['IMAGE_ATTRIBUTES']['CLOUD_COVER']} Cloud Cover")
            print(f"rm -r ./{j['LANDSAT_METADATA_FILE']['PRODUCT_CONTENTS']['LANDSAT_PRODUCT_ID']}")
            cloud_scenes.append(j['LANDSAT_METADATA_FILE']['PRODUCT_CONTENTS']['LANDSAT_PRODUCT_ID'])

# print(cloud_scenes)