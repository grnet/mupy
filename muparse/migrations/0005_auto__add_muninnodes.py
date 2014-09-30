# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MuninNodes'
        db.create_table('muparse_muninnodes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('cgi_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image_path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('munin_version', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('muparse', ['MuninNodes'])


    def backwards(self, orm):
        # Deleting model 'MuninNodes'
        db.delete_table('muparse_muninnodes')


    models = {
        'muparse.graph': {
            'Meta': {'ordering': "['name']", 'object_name': 'Graph'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.GraphCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'muparse.graphcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'GraphCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'muparse.muninnodes': {
            'Meta': {'object_name': 'MuninNodes'},
            'cgi_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'munin_version': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'muparse.node': {
            'Meta': {'ordering': "['name']", 'object_name': 'Node'},
            'graphs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['muparse.Graph']", 'null': 'True', 'through': "orm['muparse.NodeGraphs']", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.NodeGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'muparse.nodegraphs': {
            'Meta': {'object_name': 'NodeGraphs'},
            'baseurl': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.Graph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.Node']"}),
            'pageurl': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'muparse.nodegroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'NodeGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'muparse.savedsearch': {
            'Meta': {'object_name': 'SavedSearch'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'graphs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['muparse.NodeGraphs']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['muparse']