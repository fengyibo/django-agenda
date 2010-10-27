from django.conf.urls.defaults import *
from django.conf import settings
from models import * 

urlpatterns = patterns('agenda.views',
    (r'^agenda/(?P<agenda_id>\d+)/$', 'view_date'),
#    (r'^documentos/(?P<slug_cat>[-\w]+)/$', 'subcategoria_lista'),
#    (r'^documentos/(?P<slug_cat>[-\w]+)/(?P<slug_subcat>[-\w]+)/$', 'archivo_lista'),
#    (r'^documentos/(?P<slug_cat>[-\w]+)/(?P<slug_subcat>[-\w]+)/(?P<archivo_slug>[-\w]+)$', 'archivo_detalle'),
)
