# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'NodeGroup'
        db.create_table('muparse_nodegroup', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('muparse', ['NodeGroup'])

        # Adding model 'GraphCategory'
        db.create_table('muparse_graphcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('muparse', ['GraphCategory'])

        # Adding model 'Graph'
        db.create_table('muparse_graph', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['muparse.GraphCategory'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('muparse', ['Graph'])

        # Adding model 'Node'
        db.create_table('muparse_node', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['muparse.NodeGroup'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('muparse', ['Node'])

        # Adding model 'NodeGraphs'
        db.create_table('muparse_nodegraphs', (
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['muparse.Node'])),
            ('graph', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['muparse.Graph'])),
            ('pageurl', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('baseurl', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('muparse', ['NodeGraphs'])

        # Adding model 'SavedSearch'
        db.create_table('muparse_savedsearch', (
            ('display_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('muparse', ['SavedSearch'])

        # Adding M2M table for field graphs on 'SavedSearch'
        db.create_table('muparse_savedsearch_graphs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('savedsearch', models.ForeignKey(orm['muparse.savedsearch'], null=False)),
            ('nodegraphs', models.ForeignKey(orm['muparse.nodegraphs'], null=False))
        ))
        db.create_unique('muparse_savedsearch_graphs', ['savedsearch_id', 'nodegraphs_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'NodeGroup'
        db.delete_table('muparse_nodegroup')

        # Deleting model 'GraphCategory'
        db.delete_table('muparse_graphcategory')

        # Deleting model 'Graph'
        db.delete_table('muparse_graph')

        # Deleting model 'Node'
        db.delete_table('muparse_node')

        # Deleting model 'NodeGraphs'
        db.delete_table('muparse_nodegraphs')

        # Deleting model 'SavedSearch'
        db.delete_table('muparse_savedsearch')

        # Removing M2M table for field graphs on 'SavedSearch'
        db.delete_table('muparse_savedsearch_graphs')
    
    
    models = {
        'muparse.graph': {
            'Meta': {'object_name': 'Graph'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.GraphCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'muparse.graphcategory': {
            'Meta': {'object_name': 'GraphCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'muparse.node': {
            'Meta': {'object_name': 'Node'},
            'graphs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['muparse.Graph']", 'null': 'True', 'through': "orm['muparse.NodeGraphs']", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.NodeGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'muparse.nodegraphs': {
            'Meta': {'object_name': 'NodeGraphs'},
            'baseurl': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'graph': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.Graph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['muparse.Node']"}),
            'pageurl': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'muparse.nodegroup': {
            'Meta': {'object_name': 'NodeGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
