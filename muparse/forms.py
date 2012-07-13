from django import forms
from django.forms import ModelForm
from mupy.muparse.models import *
 
class SavedSearchForm(ModelForm):
    class Meta:
        model = SavedSearch
