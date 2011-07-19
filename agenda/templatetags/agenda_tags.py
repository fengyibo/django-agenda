from django.template import Library
from agenda.models import  Event

register = Library()

@register.inclusion_tag('agenda/tags/dummy.html')
def event_list_for(instance, element_number = 10 template='agenda/tags/event_list.html'):
    events = Event.objects.find_by_owner(instance)[:element_number]
    return {'template': template, 
            'events': events}
