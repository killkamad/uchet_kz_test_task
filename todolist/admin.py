from django.contrib import admin

from todolist.models import Task, User

admin.site.register(Task)
admin.site.register(User)
