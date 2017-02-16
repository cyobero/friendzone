from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class MessageManager(models.Manager):
    def create_message(self, sender, recepient, content):
        message = self.create(sender=sender, recepient=recepient, content=content)
        return message


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    recepient = models.ForeignKey(User, related_name='recepient')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = MessageManager()

    def __unicode__(self):
        return self.sender.username
