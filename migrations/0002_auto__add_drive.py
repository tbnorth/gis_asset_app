# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Drive'
        db.create_table('drive', (
            ('drive', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('machine', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('share', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('last_scanned', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('gis_asset', ['Drive'])


    def backwards(self, orm):
        
        # Deleting model 'Drive'
        db.delete_table('drive')


    models = {
        'gis_asset.asset': {
            'Meta': {'object_name': 'Asset', 'db_table': "'asset'"},
            'asset': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'format': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gis_asset.Format']", 'symmetrical': 'False'}),
            'geom_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gis_asset.Geom_type']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'records': ('django.db.models.fields.IntegerField', [], {})
        },
        'gis_asset.attr_type': {
            'Meta': {'object_name': 'Attr_type', 'db_table': "'attr_type'"},
            'attr_type': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'gis_asset.attribute': {
            'Meta': {'object_name': 'Attribute', 'db_table': "'attribute'"},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gis_asset.Asset']", 'db_column': "'asset'"}),
            'attr_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gis_asset.Attr_type']", 'db_column': "'attr_type'"}),
            'attribute': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'gis_asset.bounds': {
            'Meta': {'object_name': 'Bounds', 'db_table': "'bounds'"},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gis_asset.Asset']", 'db_column': "'asset'"}),
            'bounds': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxx': ('django.db.models.fields.FloatField', [], {}),
            'maxy': ('django.db.models.fields.FloatField', [], {}),
            'minx': ('django.db.models.fields.FloatField', [], {}),
            'miny': ('django.db.models.fields.FloatField', [], {}),
            'srid': ('django.db.models.fields.IntegerField', [], {})
        },
        'gis_asset.drive': {
            'Meta': {'object_name': 'Drive', 'db_table': "'drive'"},
            'drive': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scanned': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'letter': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'machine': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'share': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'gis_asset.format': {
            'Meta': {'object_name': 'Format', 'db_table': "'format'"},
            'format': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'gis_asset.geom_type': {
            'Meta': {'object_name': 'Geom_type', 'db_table': "'geom_type'"},
            'geom_type': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'gis_asset.path': {
            'Meta': {'object_name': 'Path', 'db_table': "'path'"},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gis_asset.Asset']", 'db_column': "'asset'"}),
            'path': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path_txt': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        }
    }

    complete_apps = ['gis_asset']
