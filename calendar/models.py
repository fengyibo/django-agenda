from django.db import models
from django.contrib.auth.models import User
from djanto.utils.translation import ugettext as _

class Calendar(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('calendar')

class Event(models.Model):
    '''Event class to make a simple event 
       inspired in django-schedule'''
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    start = models.DateTimeField(_('start'),autonow = True)
    end = models.DateTimeField(_('end'))
    created_on = models.DateTimeField(_('created_on'), default=datetime.datetime.now)
    onwner = models.models.ForeignKey(user)
    calendar = models.ForeignKey(Calendar)

    def get_absolute_url(self):
        pass

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
