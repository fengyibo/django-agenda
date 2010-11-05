from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import simplejson
import datetime
import time

class Agenda(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    public = models.BooleanField(default=False)

    def get_events(self, start, end):
        return Event.objects.filter(start__gt = start, 
                end__lt = end, agenda = self)

    def get_shared_events(self, start, end):
        return SharedEvent.objects.filter(event__start__gt = start, 
                event__end__lt = end, participant = self.owner)

    def __unicode__(self):
        return '%s - %s' % (self.name, self.owner.username)

    class Meta:
        verbose_name = _('agenda')

class Event(models.Model):
    '''Event class to make a simple event 
       inspired in django-schedule'''
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    start = models.DateTimeField(_('start'), default=datetime.datetime.now())
    end = models.DateTimeField(_('end'))
    created_on = models.DateTimeField(_('created_on'), auto_now = True)
    owner = models.ForeignKey(User)
    agenda = models.ForeignKey(Agenda)

    def get_absolute_url(self):
        pass

    def __unicode__(self):
        return self.title
    
    def to_dict(self):
        dicc = {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'start': time.mktime(self.start.timetuple()),
                'end': time.mktime(self.end.timetuple()),
                'created_on': time.mktime(self.created_on.timetuple()),
                'owner': self.owner.username,
                'agenda': self.agenda.id,
                'shared': False,
                }
        return dicc

    def to_json(self):
        return simplejson.dumps(self.to_dict())

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

class SharedEvent(models.Model):
    '''Intermediate model to share events
       the new_event field is used as flag for 
       notifications'''
    event = models.ForeignKey(Event)
    participant = models.ForeignKey(User)
    attending = models.BooleanField(default=True)
    new_event = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.event.title, 
                self.participant, self.attending)

    def get_absolute_url(self):
        pass

    def to_dict(self):
        dicc = {
                'id': self.event.id,
                'title': self.event.title,
                'description': self.event.description,
                'start': time.mktime(self.event.start.timetuple()),
                'end': time.mktime(self.event.end.timetuple()),
                'created_on': time.mktime(self.event.created_on.timetuple()),
                'owner': self.event.owner.username,
                'agenda': self.event.agenda.id,
                'shared': True,
                'attending': self.attending,
                'new_event': self.new_event,
                'className': 'fc-shared-event',
                }
        return dicc

    def to_json(self):
        return simplejson.dumps(self.to_dict())

    def unflag(self):
        self.new_event = False


    class Meta:
        verbose_name = _('shared event')
        verbose_name_plural = _('shared event')
