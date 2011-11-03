"""Load data to gis_asset.models from gisspider"""

import gispider
from models import *

import os
from datetime import datetime

for i in gispider.search_path(
    '/home/tbrown/Desktop/Proj/BirdAtlas/',
    use_gdal=False, use_dir=False, extensions=['.dbf']):
        
    assert i['path'].lower().endswith('.dbf')
    
    name = i['layer']
    extant = Asset.objects.filter(name=name, path__path_txt=i['path'])
    
    if extant.exists():
        print name, 'already'
        continue
    
    table_info = gispider.OgrFinder.get_table_info(i['path'])

    asset = Asset()
    asset.name = name
    asset.records = table_info['records']
    mod = datetime.utcfromtimestamp(os.stat(i['path']).st_mtime)
    asset.modified = mod
    asset.save()
    
    path = Path()
    path.asset = asset
    path.path_txt = i['path']
    path.save()
    
    print asset.name, 'created'
