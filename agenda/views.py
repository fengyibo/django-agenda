from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.contrib.admin.views.decorators import staff_member_required

import datetime
from models import *
from forms import *

def create_agenda(request):
    form = AgendaForm()
    return render_to_response('agenda/create_agenda.html', 
            context_instance = RequestContext(request))

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.can_be_viewed(request.user) or event.status == '1':
        return render_to_response('agenda/event_detail.html',
                {'event': event},
                context_instance = RequestContext(request))
    else:
        raise Http404

def view_date(request, agenda_id):
    '''used for calendar view'''

    if request.is_ajax():
        start = datetime.datetime.fromtimestamp(float(request.GET['start']))
        end = datetime.datetime.fromtimestamp(float(request.GET['end']))

        agenda = get_object_or_404(Agenda, pk=agenda_id) 
        eventos = []
        for event in agenda.get_events(start, end):
            eventos.append(event.to_dict())

        for event in agenda.get_shared_events(start, end, request.user.username):
            eventos.append(event.to_dict())
        
        return HttpResponse(simplejson.dumps(eventos), mimetype='application/json')
    else:
        return render_to_response('agenda/view_date.html', context_instance = RequestContext(request))

def create_event(request, agenda_id):
    '''Create event view.
       by default it will check if the user 
       can create an event'''
    if request.method == 'POST':
       agenda = get_object_or_404(Agenda = agenda_id)
       form = EditForm(request.POST)
       if form.is_valid() and agenda.is_owner(request.user):
           event = form.save(commit=False)
           event.agenda = agenda
           event.save()
           return redirect('agenda_view_date', agenda_id = agenda_id)
       else:
           error_message = _('can not create event if you are not the owner of the agenda')
           return render_to_response('create_edit.html', {'form': form})
    else:
       form = EditForm()
       return render_to_response('create_edit.html', {'form': form}, 
               context_instance=RequestContext(request))

def delete_event(request, id):
    '''Delete an event'''
    #TODO: checar permisos
    event = get_object_or_404(Event, id=id)
    if request.user.is_authenticated() and event.agenda.is_owner(request.user):
        if request.is_ajax():
            event.delete()
            return HttpResponse('deleted')
        else:
            event.delete()
            #redirect a algun lado
    else:
        raise Http404

@staff_member_required
def admin_update(request, content_type_id):
    content_type = get_object_or_404(ContentType, id= content_type_id)
    model = content_type.model_class()
    results = []
    for instance in models.objects.all():
        results.append((instance.id, instance.__unicode__()))

    return HttpResponse(simplejson.dumps(results), mimetype='application/json')
