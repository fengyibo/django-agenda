from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.contrib.auth.decorators import login_required 
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

@login_required
def create_event(request, agenda_id):
    '''Create event view.
       by default it will check if the user 
       can create an event'''
    agenda = get_object_or_404(Agenda, id = int(agenda_id))
    if request.method == 'POST':
       instance =  Event(agenda = agenda)
       form = EventForm(request.POST, instance=instance)
       if form.is_valid() and agenda.is_owner(request.user):
           event = form.save(commit=False)
           event.agenda = agenda
           event.save()
           return redirect('agenda_view_date', agenda_id = agenda_id)
       else:
           error_message = _('can not create event if you are not the owner of the agenda')
           return render_to_response('agenda/create_edit_event.html', 
                                     {'form': form, 
                                      'error_message': error_message},
                                     context_instance=RequestContext(request))
    else:
       instance =  Event(agenda = agenda)
       form = EventForm(instance = instance)
       return render_to_response('agenda/create_edit_event.html', {'form': form}, 
               context_instance=RequestContext(request))

@login_required
def edit_event(request, event_id):
    '''Create event view.
       by default it will check if the user 
       can create an event'''
    event = get_object_or_404(Event, id = int(event_id))
    if request.method == 'POST':
       form = EventForm(request.POST, instance=event)
       if form.is_valid() and event.agenda.is_owner(request.user):
           event = form.save()
           return redirect('agenda_view_date', agenda_id = event.agenda.id)
       else:
           error_message = _('can not edit event if you are not the owner of the agenda')
           return render_to_response('agenda/create_edit_event.html', 
                                     {'form': form, 
                                      'error_message': error_message},
                                     context_instance=RequestContext(request))
    else:
       form = EventForm(instance = event)
       return render_to_response('agenda/create_edit_event.html', {'form': form}, 
               context_instance=RequestContext(request))

@login_required
def share_event(request, event_id):
    event = get_object_or_404(Event, pk=id)
    if request.method == "POST":
        form = EventInviteForm(request.POST)
        if form.is_valid() and event.agenda.is_owner(request.user):
            for user in form.clean_values['users']:
                invite = EventInvite(from_user=request.user,
                                     to_user = user,
                                     event = event)
                invite.save()
        else:
            return render_to_response('agenda/share_event.html', 
                                      {'form': form, 'event': event},
                                      context_instance=RequestContext(request))
    else:
        form = EventInviteForm()
        return render_to_response('agenda/share_event.html', 
                                  {'form': form, 'event': event},
                                  context_instance=RequestContext(request))

@login_required
def event_inbox(request):
    '''inbox for invites for another events'''
    invites = EventInvite.objects.filter(to_user=request.user)
    return render_to_response('agenda/share_event.html', 
                              {'form': form, 'event': event},
                              context_instance=RequestContext(request))

@login_required
def delete_event(request, event_id):
    '''Delete an event'''
    event =  get_object_or_404(Event, pk=event_id)
    agenda_id = event.agenda.id
    if event.agenda.is_owner(request.user):
        event.delete()
        return redirect('agenda_view_date', agenda_id = agenda_id)
    else:
        #TODO: mandar mensaje
        return redirect('agenda_view_date', agenda_id = agenda_id)

@staff_member_required
def admin_update(request, content_type_id):
    '''Used in the admin to update content type'''
    content_type = get_object_or_404(ContentType, id= content_type_id)
    model = content_type.model_class()
    results = []
    for instance in model.objects.all():
        results.append((instance.id, instance.__unicode__()))

    return HttpResponse(simplejson.dumps(results), mimetype='application/json')
