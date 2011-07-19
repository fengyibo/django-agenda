from django.conf.urls.defaults import *
from django.conf import settings
from models import * 

urlpatterns = patterns('agenda.views',
    url(r'^agenda/(?P<agenda_id>\d+)/$', 'view_date', name='agenda_view_date'),
    url(r'^event/(?P<event_id>\d+)/$', 'event_detail', name='agenda_event_detail'),
    #url(r'^agenda/(?P<agenda_id>\d+)/create-event/$', 'create_agenda', name='agenda_create_event'),
    #url(r'^agenda/new/$', 'create_event', name='agenda_create_event'),
)
