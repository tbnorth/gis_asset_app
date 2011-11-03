"""Load data to gis_asset.models from gisspider"""

import gispider
from models import *

import os
from datetime import datetime

DIR='/home/tbrown/Desktop/Proj/BirdAtlas/'
DIR='/home/tbrown/n/proj/'
DIR='/home/tbrown/s/arc1/hdrive/'

def cull_dupes():
    """find repeated path_txt values and delete the corresponding
    assets, leaving only the asset with the highest pk"""
    
    multi_path = Path.objects.values('path_txt').annotate(
        pc=Count('path_txt')).exclude(pc=1)
    
    for multi in multi_path:
        assets = Asset.objects.filter(path__path_txt=multi['path_txt'])
        print assets.count(), multi['path_txt']
        maxpk = max([i.pk for i in assets])
        for a in assets:
            if a.pk == maxpk:
                continue
            a.delete()

def main():
    for i in gispider.search_path(
        DIR,
        use_gdal=False, use_dir=False, extensions=['.dbf']):
            
        assert i['path'].lower().endswith('.dbf')
        
        name = i['layer'].lower()
        
        p = i['path']
        p = p.replace('/home/tbrown/n/', '/nrgisl/')
        p = p.replace('/home/tbrown/s','')
        
        extant = Asset.objects.filter(name=name, path__path_txt=p)
        
        if extant.exists():
            print name, 'already'
            continue
            
        print i['path']
        raise Exception('all done')
        
        table_info = gispider.OgrFinder.get_table_info(i['path'])
    
        asset = Asset()
        asset.name = name
        asset.records = table_info['records']
        mod = datetime.utcfromtimestamp(os.stat(i['path']).st_mtime)
        asset.modified = mod
        
        asset.save()
        
        format, new = Format.objects.get_or_create(name=i['format'].lower())
        asset.format.add(format)
        
        geom_type, new = Geom_type.objects.get_or_create(name=i['geomText'].lower())
        asset.geom_type.add(geom_type)
        
        path = Path()
        path.asset = asset
        path.path_txt = p
        path.save()
        
        for a in table_info['attrib']:
            aname = a['name'].lower()
            try:
                unicode(aname)  # check it's ok for DB
                attr_type, new = Attr_type.objects.get_or_create(name=a['type'].lower())
                attr = Attribute()
                attr.asset = asset
                attr.attr_type = attr_type
                attr.name = aname
                attr.save()
                print 'attrib.', attr.name
            except UnicodeDecodeError:
                pass  # ignore weird attribute names
        
        print asset.name, 'created'
