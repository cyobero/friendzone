from django import forms
import datetime
from django.utils.safestring import mark_safe
from users.models import UserProfile


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """
    This renderes the radio buttons to be aligned horizontally (the default is vertical).
    """
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class RegistrationForm(forms.Form):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    # This gives us a list of years to choose from for the birthdate field.
    year_choices = []
    now = datetime.datetime.now()

    for i in range(1900, now.year + 1):
        year_choices.append(str(i))

    year_choices = list(reversed(year_choices))  # Make the drop down field for year in descending order.

    # The required fields the user must fill out to register
    first_name = forms.CharField(label='', max_length=70, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    password_verify = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Type Password Again'
    }))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'username'
    }))
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=year_choices, attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices=gender_choices)


class SignInForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class ChangeProfilePic(forms.Form):
    picture = forms.ImageField(label='Change Profile Picture')


class EditProfile(forms.Form):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    # This gives us a list of years to choose from for the birthdate field.
    year_choices = []
    now = datetime.datetime.now()

    for i in range(1900, now.year + 1):
        year_choices.append(str(i))

    year_choices = list(reversed(year_choices))  # Make the drop down field for year in descending order.

    # The required fields the user must fill out to register
    first_name = forms.CharField(label='', max_length=70, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'username'
    }))
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=year_choices, attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices=gender_choices)
    bio = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter bio here.'
    }))


class QuestionForm(forms.Form):
    title = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'What is your question?',
        'size': '70',
        'align': 'left',
        'rows': '2',
        'styl': 'display:inline-block;vertical-align:middle'
    }))
    content = forms.CharField(label='', required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter details of your question here...',
        'rows': '4',
        'style': 'display:inline-block;vertical-align:middle'
    }))


class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '4'
    }))


class MessageForm(forms.Form):
    message = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '13'
    }))


class ReplyForm(forms.Form):
    reply = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '4'
    }))