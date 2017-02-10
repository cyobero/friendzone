from django.contrib import admin

# Register your models here.
from inbox.models import Message


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)