# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Asset'
        db.create_table('asset', (
            ('asset', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('records', self.gf('django.db.models.fields.IntegerField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('gis_asset', ['Asset'])

        # Adding M2M table for field format on 'Asset'
        db.create_table('asset_format', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('asset', models.ForeignKey(orm['gis_asset.asset'], null=False)),
            ('format', models.ForeignKey(orm['gis_asset.format'], null=False))
        ))
        db.create_unique('asset_format', ['asset_id', 'format_id'])

        # Adding M2M table for field geom_type on 'Asset'
        db.create_table('asset_geom_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('asset', models.ForeignKey(orm['gis_asset.asset'], null=False)),
            ('geom_type', models.ForeignKey(orm['gis_asset.geom_type'], null=False))
        ))
        db.create_unique('asset_geom_type', ['asset_id', 'geom_type_id'])

        # Adding model 'Attr_type'
        db.create_table('attr_type', (
            ('attr_type', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal('gis_asset', ['Attr_type'])

        # Adding model 'Bounds'
        db.create_table('bounds', (
            ('bounds', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gis_asset.Asset'], db_column='asset')),
            ('srid', self.gf('django.db.models.fields.IntegerField')()),
            ('minx', self.gf('django.db.models.fields.FloatField')()),
            ('maxx', self.gf('django.db.models.fields.FloatField')()),
            ('miny', self.gf('django.db.models.fields.FloatField')()),
            ('maxy', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('gis_asset', ['Bounds'])

        # Adding model 'Path'
        db.create_table('path', (
            ('path', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gis_asset.Asset'], db_column='asset')),
            ('path_txt', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal('gis_asset', ['Path'])

        # Adding model 'Attribute'
        db.create_table('attribute', (
            ('attribute', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gis_asset.Asset'], db_column='asset')),
            ('attr_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gis_asset.Attr_type'], db_column='attr_type')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal('gis_asset', ['Attribute'])

        # Adding model 'Format'
        db.create_table('format', (
            ('format', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal('gis_asset', ['Format'])

        # Adding model 'Geom_type'
        db.create_table('geom_type', (
            ('geom_type', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal('gis_asset', ['Geom_type'])


    def backwards(self, orm):
        
        # Deleting model 'Asset'
        db.delete_table('asset')

        # Removing M2M table for field format on 'Asset'
        db.delete_table('asset_format')

        # Removing M2M table for field geom_type on 'Asset'
        db.delete_table('asset_geom_type')

        # Deleting model 'Attr_type'
        db.delete_table('attr_type')

        # Deleting model 'Bounds'
        db.delete_table('bounds')

        # Deleting model 'Path'
        db.delete_table('path')

        # Deleting model 'Attribute'
        db.delete_table('attribute')

        # Deleting model 'Format'
        db.delete_table('format')

        # Deleting model 'Geom_type'
        db.delete_table('geom_type')


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
