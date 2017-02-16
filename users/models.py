from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import datetime


def upload_location(user, filename):
    """
    Saves image to media directory and creates a folder with user's username and keeps original file name unchanged.
    """
    return '%s/%s' % (user.user_id, filename)


class UserProfile(models.Model):
    # Link UserProfile model to User model instance
    user = models.OneToOneField(User)

    # Additional user information
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    gender = models.CharField(max_length=6, choices=gender_choices, null=True)
    birth_date = models.DateField()
    profile_pic = models.ImageField(upload_to=upload_location, default='default.jpg')
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField('UserProfile', related_name='following')

    def get_username(self):
        return self.user.username

    def calculate_age(self):
        user_birthdate = '%s/%s/%s' % (str(self.birth_date.year), str(self.birth_date.month), str(self.birth_date.day))
        user_birthdate = datetime.datetime.strptime(user_birthdate, '%Y/%m/%d')
        today = datetime.datetime.today()
        age = (today - user_birthdate).days/365.2424

        return int(age)

    def __unicode__(self):
        return self.user.username
