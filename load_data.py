"""Load data to gis_asset.models from gisspider

To update passwords
set search_path to nrgisl;
\set oldpass '''Kelsie1234'''
\set newpass '''0PetNames'''

update drive
   set "user" = regexp_replace("user", :oldpass, :newpass)
 where "user" ~ :oldpass
;

"""

import glob
import json
import os
import ping
import socket
import sys
from datetime import datetime, date

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gis_asset_ws.settings")
import django
django.setup()

from gis_asset_app.models import *
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

    try:
        dns_ip = socket.gethostbyname(host)
    except socket.gaierror:
        dns_ip = None

    if dns_ip:
        p = ping.Ping(dns_ip)
        p.run(1)
        if p.receive_count != 1:
            print "Could not ping host, will try stored IP if available"
            if drive.ip:
                host = drive.ip
    else:
        print "Host lookup failed, will try stored IP if available"
        if drive.ip:
            host = drive.ip

    user, password = drive.user, None
    if ':' in user:
        user, password = user.split(':')

    opt = 'user='+user
    if password is not None:
        opt += ',password='+password

    cmd = 'mount.cifs //%s/%s %s -o %s' % (
        host, drive.share, mp, opt)

    os.system(cmd)

    if len(glob.glob(mp+'/*')) == 0:
        raise Exception("Mount point '%s' has NO content\n(%s)"%(mp,cmd))

    return mp
def main():

    if len(sys.argv) > 1:
        return load_file(int(sys.argv[1]), sys.argv[2])

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
        for i in gispider.search_path(
            mount_path,
            use_gdal_on=('dir', 'file'), # 'dir',
            use_ogr_on=('file',), # 'file',
            ogr_extensions=['.dbf', '.shp', '.kml', '.gpx', ],
            ):

            proc_record(drive, i)

    finally:
        unmount_drive(drive)


    drive.last_scanned = date.today()
    drive.save()
def load_file(drive_id, filepath):
    """load_file - Load spider records from filepath and apply to drive

    :param int drive_id: PK of drive
    :param str filepath: path to spider file
    """
    drive = Drive.objects.get(pk=drive_id)
    records = json.load(open(filepath))
    for record in records:
        proc_record(drive, record)
def proc_record(drive, i):
    # assert i['path'].lower().endswith('.dbf')
    if i['path'].lower().endswith('.shp'):
        return

    name = i['name'].lower()

    vis_path = "/%s/%s" % (drive.machine, drive.share)
    p = i['path'] # .replace(mount_path, vis_path)

    if Path.objects.filter(path_txt=p).exists():
        print name, 'already'
        return

    print p

    table_info = i['table_info']

    if 'records' not in table_info:
        return

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

    if 'GDAL' in i['find_type']:
        bounds = Bounds()
        for attr in ('srid', 'minx', 'maxx', 'miny', 'maxy', 'cellsx', 'cellsy',
            'sizex', 'sizey'):
            if attr == 'srid':
                setattr(bounds, attr, i[attr])
            else:
                # postgresql_psycopg2 will choke on 0.00<180 more 0s>008931279, so float()
                # setattr(bounds, attr, float(i[attr]))
                # seems the problem is the size of the exponent, not the conversion, so
                setattr(bounds, attr, round(float(i[attr]), 12))
        bounds.asset = asset
        bounds.save()

    print asset.name, 'created'
if __name__ == '__main__':
    main()
