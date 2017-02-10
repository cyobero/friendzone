from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile


class PostManager(models.Manager):
    def create_post(self, title, author, content):
        post = self.create(
            title = title,
            author = author,
            content = content
        )

        return post


class Post(models.Model):
    title = models.CharField(max_length=145)
    author = models.ForeignKey(User)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    tags = models.CharField(max_length=75, null=True)
    anonymous = models.BooleanField(default=False)

    objects = PostManager()

    def truncate_content(self):
        if len(self.content) > 250:
            return self.content[:250] + "..."
        else:
            return self.content

    def get_absolute_url(self):
        return '/%s/post/%i/' % (self.author.username, self.id)

    def get_img_thumbnail(self):
        author = self.author_id
        user_profile = UserProfile.objects.get(user=author)
        img_thumbnail = user_profile.profile_pic.url

        return img_thumbnail

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp', ]