from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.translation import ugettext as _

import datetime
import json
from models import *
from forms import *

fecha = datetime.datetime.now()

def ver_dia(request):
    fecha = datetime.datetime.now()   
    
    if request.is_ajax():
        start = datetime.datetime.fromtimestamp(float(request.GET['start']))
        end = datetime.datetime.fromtimestamp(float(request.GET['end']))
        fecha1 = datetime.date(start.year, start.month, start.day)
        fecha2 = datetime.date(end.year, end.month, end.day)
        
        citas1 = Citas.objects.filter(fecha__range=(fecha1, fecha2))
        var = []        
        for c in citas1:
            d = {'id':"", 'title':"", 'start':"", 'end':None, 'allDay': None}
            d["id"]=str(c.id)
            d["title"]=str(c.trabajo_realizar)+' a '+str(c.cliente)
            d["start"]=str(c.fecha)+' '+str(c.hora_ini)
            d["end"]=str(c.fecha)+' '+str(c.hora_fin)
            d['allDay']=False
            var.append(d)
        return HttpResponse(json.dumps(var), mimetype='application/json')
    
    return render_to_response('ver_dia.html', RequestContext(request, locals()))

def view_date(request, agenda_id):

    if request.is_ajax():
        start = datetime.datetime.fromtimestamp(float(request.GET['start']))
        end = datetime.datetime.fromtimestamp(float(request.GET['end']))
        
     

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
