from django.contrib import admin
from muparse.models import *
from django.contrib.auth.models import User
from accounts.models import *
from django.conf import settings
from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class NodeForm(ModelForm):
    nodes=forms.ModelMultipleChoiceField(Node.objects.all(),widget=
            FilteredSelectMultiple("Node",True), required=False)
    class Meta:
        model= UserProfile

class UserNodeGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_nodes')
    form = NodeForm


admin.site.register(UserProfile, UserNodeGroupAdmin)
