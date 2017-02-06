from django.contrib import admin
from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment, CommentAdmin)