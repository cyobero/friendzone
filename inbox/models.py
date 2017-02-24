from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class MessageManager(models.Manager):
    def all(self):
        query_set = super(MessageManager, self).filter(parent=None)
        return query_set

    def create_message(self, sender, recepient, content, parent):
        message = self.create(sender=sender, recepient=recepient, content=content, parent=parent)
        return message


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    recepient = models.ForeignKey(User, related_name='recepient')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='parent_message')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = MessageManager()

    def truncate_content(self):
        if len(self.content) > 60:
            return str(self.content[:60]) + '...'
        return self.content

    def children(self):  # Replies
        return Message.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def __unicode__(self):
        return self.sender.username

    class Meta:
        ordering = ['-timestamp', ]
