from django.contrib import admin
from mupy.muparse.models import *
from django.contrib.auth.models import User
from mupy.accounts.models import *
from django.conf import settings
from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class NodeGroupAdminForm(ModelForm):
    nodegroups=forms.ModelMultipleChoiceField(NodeGroup.objects.all(),widget=
            FilteredSelectMultiple("NodeGroup",True), required=False)
    class Meta:
        model= UserProfile

class UserNodeGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_nodegroups')
    form = NodeGroupAdminForm


admin.site.register(UserProfile, UserNodeGroupAdmin)