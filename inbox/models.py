from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    recepient = models.ForeignKey(User, related_name='recepient')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.sender