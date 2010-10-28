from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import simplejson

import datetime
from models import *
from forms import *

fecha = datetime.datetime.now()

def view_date(request, agenda_id):

    if request.is_ajax():
        start = datetime.datetime.fromtimestamp(float(request.GET['start']))
        end = datetime.datetime.fromtimestamp(float(request.GET['end']))

        agenda = get_object_or_404(Agenda, pk=agenda_id) 
        eventos = []
        for event in agenda.get_events(start, end):
            eventos.append(event.to_dict())

        for event in agenda.get_shared_events(start, end):
            eventos.append(event.to_dict())
        
        return HttpResponse(simplejson.dumps(eventos), mimetype='application/json')
    return render_to_response('agenda/view_date.html', RequestContext(request))

def editar(request, id):
    boton = 'eliminar'
    cita = Citas.objects.get(id=id)
    form = EditForm(instance=cita)
    if request.method == 'POST':
        form = EditForm(data=request.POST, instance=cita)
        if form.is_valid():            
            form.save()
            return HttpResponse('OK')        
    else:
        form = EditForm(instance=cita)        
    return render_to_response('agregarEditar.html', RequestContext(request, locals()))

def create_event(request, agenda_id):
    '''Create event view.
       by default it will check if the user 
       can create an event'''
    button_text = _('Cancel')
    if request.method == 'POST':
       form = EditForm(request.POST)
       if form.is_valid():
           event = form.save(commit=False)
           event.agenda= get_object_or_404(Agenda = agenda_id) 
           event.save()
           return HttpResponse('OK')
       else:
           return HttpResponse('OMFG')
    else:
       form = EditForm()
       return render_to_response('create_edit.html', {'button_text': button_text})

def delete_event(request, id):
    '''Delete an event'''
    #TODO: checar permisos
    if request.is_ajax():
        event = get_object_or_404(Event, id=id)
        event.delete()
        return HttpResponse('deleted')

def cambiar_fechas(request):    
    if request.is_ajax():
        id = request.POST['id']
        cita = Citas.objects.get(id=id)
        cita.hora_ini = request.POST['start']
        cita.hora_fin = request.POST['end']
        cita.fecha = request.POST['fecha']
        cita.save()        
        return HttpResponse('Cambios realizados')
      
    else:
        return HttpResponse('ERROR')
    
    return HttpResponse('ERROR')        
