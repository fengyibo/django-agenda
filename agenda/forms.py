from django import forms as forms
from django.forms.extras.widgets import *
from django.utils.translation import ugettext as _

from models import *

class EventForm(forms.ModelForm):
    class Meta:
        model = Event 

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda 

class EventInviteForm(forms.ModelForm):
    date_created = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    from_user = forms.ModelChoiceField(queryset= User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = EventInvite 

class AgendaAdminForm(forms.ModelForm):
    object_id = forms.ChoiceField(label=_('object'), choices=(('','----'),('1', '------')))

    class Meta:
        model = Agenda
