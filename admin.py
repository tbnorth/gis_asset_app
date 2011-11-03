# from django.contrib.gis import admin
from models import *
from django.contrib import admin

admin.site.register(Asset)
admin.site.register(Attr_type)
admin.site.register(Attribute)
admin.site.register(Path)
admin.site.register(Bounds)
admin.site.register(Geom_type)
admin.site.register(Format)
