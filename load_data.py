"""Load data to gis_asset.models from gisspider"""

import gispider
from models import *

import os
import glob
from datetime import datetime, date
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

def mount_path(drive):
    
    mp = "~/ga_mounts/%s_%s" % (
        drive.machine,
        drive.share.replace('/', '_')
    )
    
    mp = os.path.realpath(os.path.expanduser(mp))
    
    return mp
    
def unmount_drive(drive):
    
    mp = mount_path(drive)
    
    #X os.system('umount.cifs %s' % mp)
    os.system('umount %s' % mp)
    
    if len(glob.glob(mp+'/*')) != 0:
        raise Exception("Mount point '%s' STILL has content"%mp)    
    
    
def mount_drive(drive):
    
    mp = mount_path(drive)
    
    if not os.path.exists(mp):
        os.makedirs(mp)
    
    if len(glob.glob(mp+'/*')) != 0:
        raise Exception("Mount point '%s' has content ALREADY"%mp)
    
    host = "%s.nrri.umn.edu" % drive.machine
    
    user, password = drive.user, None
    if ':' in user:
        user, password = user.split(':')
    
    opt = 'user='+user
    if password is not None:
        opt += ',password='+password
    
    os.system('mount.cifs //%s/%s %s -o %s' % (
        host, drive.share, mp, opt))
    
    if len(glob.glob(mp+'/*')) == 0:
        raise Exception("Mount point '%s' has NO content"%mp)
        
    return mp
def main():
    
    for i in Drive.objects.order_by('pk'):
        print "%2d: %s" % (i.pk, i)
    
    pk = raw_input("Which: ")
    
    for i in pk.split():
        scan_drive(int(i))
        
def scan_drive(pk):
    
    drive = Drive.objects.get(pk=pk)
    
    mount_path = mount_drive(drive)
    
    vis_path = "/%s/%s" % (drive.machine, drive.share)
    
    try:
        for i in gispider.search_path(mount_path,
            use_gdal=False, use_dir=False, extensions=['.dbf']):
                
            assert i['path'].lower().endswith('.dbf')
            
            name = i['layer'].lower()

            p = i['path'].replace(mount_path, vis_path)
            
            if Path.objects.filter(path_txt=p).exists():
                print name, 'already'
                continue
            
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
                    # print 'attrib.', attr.name
                except UnicodeDecodeError:
                    pass  # ignore weird attribute names
            
            print asset.name, 'created'
            
        drive.last_scanned = date.today()
        drive.save()
            
    finally:
        unmount_drive(drive)
