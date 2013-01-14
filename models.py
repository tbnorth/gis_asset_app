# AUTOMATICALLY GENERATED MODELS, edit models_base.py instead

from models_base import *

from django.forms import ValidationError

from django.db.models import Min,Max,Avg,Count

# admin registrations
"""
admin.site.register(Asset)
admin.site.register(Attr_type)
admin.site.register(Bounds)
admin.site.register(Path)
admin.site.register(Attribute)
admin.site.register(Format)
admin.site.register(Geom_type)
admin.site.register(Drive)
"""

import re
_fp0=re.compile(r'[[\]\r\n\t;: /\\"\'!?*&^%@#$|{}()~`<>=]+')
def fix_path(s):
            return _fp0.sub('_', str(s))
def dml_dj_set_attr(table, field, attr):
            for fld in table._meta.fields:
                if fld.name == field:
                    fld.dml_attr = attr
                    break
            else:
                # print "Could not find field %s in %s"%(field,table)
                pass
        
def dml_dj_add_field_validator(table, field, validator):
            for fld in table._meta.fields:
                if fld.name == field:
                    fld.validators.append(validator)
                    break
            else:
                raise Exception("Could not find field %s"%field)
        
def dml_dj_uploader(path):
            def f(self, orig, path=path):
                print  eval(path)
                return eval(path)
        
if 'md5_calc_targets' not in globals():
            md5_calc_targets = []
            def md5_calc(sender, instance, *args, **kwargs):
                if sender in md5_calc_targets:
                    DFile = instance.path
                    DFile.seek(0)
                    instance.md5 = md5.new(DFile.read()).hexdigest()
            pre_save.connect(md5_calc)
        
class Asset (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "asset"


    asset = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4096,help_text='name')
    # name
    records = models.IntegerField(help_text='records or bands')
    # records or bands
    modified = models.DateTimeField(help_text='time of last modification')
    # time of last modification
    format = models.ManyToManyField("Format")
    geom_type = models.ManyToManyField("Geom_type")


Asset.dml_attr = {'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Asset, "name", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'name'})
dml_dj_set_attr(Asset, "format", {'units': '', 'dj_m2m_target': 'format', 'dj_css_class': 'ManyToManyField', 'dj_description': ''})
dml_dj_set_attr(Asset, "modified", {'units': '', 'dj_css_class': 'DateTimeField', 'dj_description': 'time of last modification'})
dml_dj_set_attr(Asset, "records", {'units': '', 'dj_css_class': 'IntegerField', 'dj_description': 'records or bands'})
dml_dj_set_attr(Asset, "asset", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': ''})
dml_dj_set_attr(Asset, "geom_type", {'units': '', 'dj_m2m_target': 'geom_type', 'dj_css_class': 'ManyToManyField', 'dj_description': ''})

class Attr_type (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "attr_type"


    attr_type = models.AutoField(primary_key=True)
    # attribute type
    name = models.CharField(max_length=4096,help_text='name')
    # name


Attr_type.dml_attr = {'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Attr_type, "attr_type", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': 'attribute type'})
dml_dj_set_attr(Attr_type, "name", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'name'})

class Bounds (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "bounds"


    bounds = models.AutoField(primary_key=True)
    # bounding box
    asset = models.ForeignKey("Asset", db_column="asset", help_text='asset')
    # asset
    srid = models.IntegerField(blank=True, null=True, help_text='Spatial Reference ID')
    # Spatial Reference ID
    minx = models.FloatField(help_text='minx')
    # minx
    maxx = models.FloatField(help_text='maxx')
    # maxx
    miny = models.FloatField(help_text='miny')
    # miny
    maxy = models.FloatField(help_text='maxy')
    # maxy
    cellsx = models.IntegerField(blank=True, null=True, help_text='Raster cells in x axis')
    # Raster cells in x axis
    cellsy = models.IntegerField(blank=True, null=True, help_text='Raster cells in y axis')
    # Raster cells in y axis
    sizex = models.FloatField(blank=True, null=True, help_text='Raster cell x size')
    # Raster cell x size
    sizey = models.FloatField(blank=True, null=True, help_text='Raster cell y size')
    # Raster cell y size


Bounds.dml_attr = {'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Bounds, "maxx", {'units': '', 'dj_css_class': 'FloatField', 'dj_description': 'maxx'})
dml_dj_set_attr(Bounds, "maxy", {'units': '', 'dj_css_class': 'FloatField', 'dj_description': 'maxy'})
dml_dj_set_attr(Bounds, "sizex", {'units': '', 'dj_css_class': 'FloatField', 'dj_description': 'Raster cell x size'})
dml_dj_set_attr(Bounds, "bounds", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': 'bounding box'})
dml_dj_set_attr(Bounds, "sizey", {'units': '', 'dj_css_class': 'FloatField', 'dj_description': 'Raster cell y size'})
dml_dj_set_attr(Bounds, "minx", {'units': '', 'dj_css_class': 'FloatField', 'dj_description': 'minx'})
dml_dj_set_attr(Bounds, "miny", {'units': '', 'dj_css_class': 'FloatField', 'dj_description': 'miny'})
dml_dj_set_attr(Bounds, "cellsy", {'units': '', 'dj_css_class': 'IntegerField', 'dj_description': 'Raster cells in y axis'})
dml_dj_set_attr(Bounds, "cellsx", {'units': '', 'dj_css_class': 'IntegerField', 'dj_description': 'Raster cells in x axis'})
dml_dj_set_attr(Bounds, "asset", {'units': '', 'dj_css_class': 'ForeignKey', 'dj_description': 'asset'})
dml_dj_set_attr(Bounds, "srid", {'units': '', 'dj_css_class': 'IntegerField', 'dj_description': 'Spatial Reference ID'})

class Path (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "path"


    path = models.AutoField(primary_key=True)
    # path
    asset = models.ForeignKey("Asset", db_column="asset", help_text='asset')
    # asset
    path_txt = models.CharField(max_length=4096,help_text='path')
    # path


Path.dml_attr = {'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Path, "path_txt", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'path'})
dml_dj_set_attr(Path, "path", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': 'path'})
dml_dj_set_attr(Path, "asset", {'units': '', 'dj_css_class': 'ForeignKey', 'dj_description': 'asset'})

class Attribute (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "attribute"


    attribute = models.AutoField(primary_key=True)
    # attribute (column) of an asset
    asset = models.ForeignKey("Asset", db_column="asset", help_text='asset')
    # asset
    attr_type = models.ForeignKey("Attr_type", db_column="attr_type", )
    name = models.CharField(max_length=4096,help_text='name of attribute')
    # name of attribute


Attribute.dml_attr = {'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Attribute, "attribute", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': 'attribute (column) of an asset'})
dml_dj_set_attr(Attribute, "asset", {'units': '', 'dj_css_class': 'ForeignKey', 'dj_description': 'asset'})
dml_dj_set_attr(Attribute, "name", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'name of attribute'})
dml_dj_set_attr(Attribute, "attr_type", {'units': '', 'dj_css_class': 'ForeignKey', 'dj_description': ''})

class Format (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "format"


    format = models.AutoField(primary_key=True)
    # format
    name = models.CharField(max_length=4096,help_text='name')
    # name


Format.dml_attr = {'dj_m2m_target': 'format asset False', 'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Format, "name", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'name'})
dml_dj_set_attr(Format, "format", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': 'format'})

class Geom_type (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "geom_type"


    geom_type = models.AutoField(primary_key=True)
    # geometry type
    name = models.CharField(max_length=4096,help_text='name')
    # name


Geom_type.dml_attr = {'dj_m2m_target': 'geom_type asset False', 'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Geom_type, "name", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'name'})
dml_dj_set_attr(Geom_type, "geom_type", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': 'geometry type'})

class Drive (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "drive"

    def __unicode__(self):
        return "%s: scanned %s //%s/%s" % (self.letter, self.last_scanned or 'never', self.machine, self.share)

    drive = models.AutoField(primary_key=True)
    # drive
    letter = models.CharField(max_length=4096,help_text='drive letter')
    # drive letter
    machine = models.CharField(max_length=4096,help_text='mount point')
    # mount point
    share = models.CharField(max_length=4096,help_text='share name')
    # share name
    last_scanned = models.DateField(blank=True, null=True, help_text='last scan date')
    # last scan date
    user = models.CharField(max_length=4096,blank=True, help_text='password:user')
    # password:user
    ip = models.CharField(max_length=4096,blank=True, help_text='IP to try if lookup fails')
    # IP to try if lookup fails


Drive.dml_attr = {'dj_name': '"%s: scanned %s //%s/%s" % (self.letter, self.last_scanned or \'never\', self.machine, self.share)', 'schema_name': 'GIS Asset index database', 'dj_description': 'NO COMMENT SUPPLIED'}

dml_dj_set_attr(Drive, "last_scanned", {'units': '', 'dj_css_class': 'DateField', 'dj_description': 'last scan date'})
dml_dj_set_attr(Drive, "ip", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'IP to try if lookup fails'})
dml_dj_set_attr(Drive, "share", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'share name'})
dml_dj_set_attr(Drive, "drive", {'units': '', 'dj_css_class': 'AutoField', 'dj_description': 'drive'})
dml_dj_set_attr(Drive, "machine", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'mount point'})
dml_dj_set_attr(Drive, "user", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'password:user'})
dml_dj_set_attr(Drive, "letter", {'units': '', 'dj_css_class': 'CharField', 'dj_description': 'drive letter'})

# bounds.asset -> asset.asset
# path.asset -> asset.asset
# attribute.asset -> asset.asset
# attribute.attr_type -> attr_type.attr_type

# load customizations
try:
    import models_post
except ImportError:
    pass


