# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Node.updated'
        db.add_column('muparse_node', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 21, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'GraphCategory.updated'
        db.add_column('muparse_graphcategory', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 21, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Graph.updated'
        db.add_column('muparse_graph', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 21, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'NodeGroup.updated'
        db.add_column('muparse_nodegroup', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 21, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Node.updated'
        db.delete_column('muparse_node', 'updated')

        # Deleting field 'GraphCategory.updated'
        db.delete_column('muparse_graphcategory', 'updated')

        # Deleting field 'Graph.updated'
        db.delete_column('muparse_graph', 'updated')

        # Deleting field 'NodeGroup.updated'
        db.delete_column('muparse_nodegroup', 'updated')


    models = {
        'muparse.graph': {
            'Meta': {'ordering': "['name']", 'object_name': 'Graph'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.GraphCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'muparse.graphcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'GraphCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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