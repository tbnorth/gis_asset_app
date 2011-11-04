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
        
class Asset (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "asset"


    asset = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4096,)
    # name
    records = models.IntegerField()
    # records or bands
    modified = models.DateTimeField()
    # time of last modification
    format = models.ManyToManyField("Format")
    geom_type = models.ManyToManyField("Geom_type")


Asset.dml_attr = {}

dml_dj_set_attr(Asset, "name", {'dj_description': 'name'})
dml_dj_set_attr(Asset, "format", {'dj_m2m_target': 'format', 'dj_description': ''})
dml_dj_set_attr(Asset, "modified", {'dj_description': 'time of last modification'})
dml_dj_set_attr(Asset, "records", {'dj_description': 'records or bands'})
dml_dj_set_attr(Asset, "asset", {'dj_description': ''})
dml_dj_set_attr(Asset, "geom_type", {'dj_m2m_target': 'geom_type', 'dj_description': ''})

class Attr_type (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "attr_type"


    attr_type = models.AutoField(primary_key=True)
    # attribute type
    name = models.CharField(max_length=4096,)
    # name


Attr_type.dml_attr = {}

dml_dj_set_attr(Attr_type, "attr_type", {'dj_description': 'attribute type'})
dml_dj_set_attr(Attr_type, "name", {'dj_description': 'name'})

class Bounds (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "bounds"


    bounds = models.AutoField(primary_key=True)
    # bounding box
    asset = models.ForeignKey("Asset", db_column="asset", )
    # asset
    srid = models.IntegerField()
    # Spatial Reference ID
    minx = models.FloatField()
    # minx
    maxx = models.FloatField()
    # maxx
    miny = models.FloatField()
    # miny
    maxy = models.FloatField()
    # maxy


Bounds.dml_attr = {}

dml_dj_set_attr(Bounds, "maxx", {'dj_description': 'maxx'})
dml_dj_set_attr(Bounds, "maxy", {'dj_description': 'maxy'})
dml_dj_set_attr(Bounds, "bounds", {'dj_description': 'bounding box'})
dml_dj_set_attr(Bounds, "minx", {'dj_description': 'minx'})
dml_dj_set_attr(Bounds, "miny", {'dj_description': 'miny'})
dml_dj_set_attr(Bounds, "asset", {'dj_description': 'asset'})
dml_dj_set_attr(Bounds, "srid", {'dj_description': 'Spatial Reference ID'})

class Path (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "path"


    path = models.AutoField(primary_key=True)
    # path
    asset = models.ForeignKey("Asset", db_column="asset", )
    # asset
    path_txt = models.CharField(max_length=4096,)
    # path


Path.dml_attr = {}

dml_dj_set_attr(Path, "path_txt", {'dj_description': 'path'})
dml_dj_set_attr(Path, "path", {'dj_description': 'path'})
dml_dj_set_attr(Path, "asset", {'dj_description': 'asset'})

class Attribute (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "attribute"


    attribute = models.AutoField(primary_key=True)
    # attribute (column) of an asset
    asset = models.ForeignKey("Asset", db_column="asset", )
    # asset
    attr_type = models.ForeignKey("Attr_type", db_column="attr_type", )
    name = models.CharField(max_length=4096,)
    # name of attribute


Attribute.dml_attr = {}

dml_dj_set_attr(Attribute, "attribute", {'dj_description': 'attribute (column) of an asset'})
dml_dj_set_attr(Attribute, "asset", {'dj_description': 'asset'})
dml_dj_set_attr(Attribute, "name", {'dj_description': 'name of attribute'})
dml_dj_set_attr(Attribute, "attr_type", {'dj_description': ''})

class Format (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "format"


    format = models.AutoField(primary_key=True)
    # format
    name = models.CharField(max_length=4096,)
    # name


Format.dml_attr = {'dj_m2m_target': 'format asset False'}

dml_dj_set_attr(Format, "name", {'dj_description': 'name'})
dml_dj_set_attr(Format, "format", {'dj_description': 'format'})

class Geom_type (models.Model):  # AUTOMATICALLY GENERATED
    """NO COMMENT SUPPLIED
    """

    class Meta:
        pass
        db_table = "geom_type"


    geom_type = models.AutoField(primary_key=True)
    # geometry type
    name = models.CharField(max_length=4096,)
    # name


Geom_type.dml_attr = {'dj_m2m_target': 'geom_type asset False'}

dml_dj_set_attr(Geom_type, "name", {'dj_description': 'name'})
dml_dj_set_attr(Geom_type, "geom_type", {'dj_description': 'geometry type'})

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
    letter = models.CharField(max_length=4096,)
    # drive letter
    machine = models.CharField(max_length=4096,)
    # mount point
    share = models.CharField(max_length=4096,)
    # share name
    last_scanned = models.DateField(blank=True, null=True)
    # last scan date
    user = models.CharField(max_length=4096,blank=True)
    # password:user


Drive.dml_attr = {'dj_name': '"%s: scanned %s //%s/%s" % (self.letter, self.last_scanned or \'never\', self.machine, self.share)'}

dml_dj_set_attr(Drive, "last_scanned", {'dj_description': 'last scan date'})
dml_dj_set_attr(Drive, "share", {'dj_description': 'share name'})
dml_dj_set_attr(Drive, "drive", {'dj_description': 'drive'})
dml_dj_set_attr(Drive, "machine", {'dj_description': 'mount point'})
dml_dj_set_attr(Drive, "user", {'dj_description': 'password:user'})
dml_dj_set_attr(Drive, "letter", {'dj_description': 'drive letter'})

# bounds.asset -> asset.asset
# path.asset -> asset.asset
# attribute.asset -> asset.asset
# attribute.attr_type -> attr_type.attr_type

# load customizations
try:
    import models_post
except ImportError:
    pass


