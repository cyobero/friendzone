from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your mnodels here
from posts.models import Post


class PostManager(models.Manager):
    def create_post(self, user, post, comment):
        post = self.create(
            user = user,
            post = post,
            comment = comment
        )

        return post


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    comment = models.TextField()
    likes = models.IntegerField(default=0, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = PostManager()

    def __unicode__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['-timestamp', ]