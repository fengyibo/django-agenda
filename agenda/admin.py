from django.contrib import admin
from django.conf import settings
from models import *
from forms import AgendaAdminForm

class AgendaAdmin(admin.ModelAdmin):
    form =  AgendaAdminForm

    class Media:
        js = ['%sagenda/js/updater.js' % settings.MEDIA_URL,]

admin.site.register(Event)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(SharedEvent)
admin.site.register(EventInvite)
