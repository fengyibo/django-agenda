from django import forms as forms
from django.forms.extras.widgets import *
from models import *

class EditForm(forms.ModelForm):       
    class Meta:
        model = Citas        
 
