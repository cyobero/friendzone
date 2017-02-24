from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import template

# Create your models here
from posts.models import Post


register = template.Library()


class CommentManager(models.Manager):
    def all(self):
        query_set = super(CommentManager, self).filter(parent=None)
        return query_set

    def create_comment(self, user, post, comment, parent):
        comment = self.create(user=user, post=post, comment=comment, parent=parent)
        return comment


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    comment = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='parent_comment')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = CommentManager()

    def get_absolute_url(self):
        return '/%s/post/%i/' % (self.post.author, self.post.id)

    def children(self):  # Replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def __unicode__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['-timestamp', ]


class Upvote(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)


@property
def sort(self):
    return self.children_set.order_by('timestamp')