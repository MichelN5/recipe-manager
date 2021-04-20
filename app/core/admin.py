from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models

class UserAdmin(BaseUserAdmin):
    ordering= ['id']
    list_display= ['name','email']
list_filter = ('admin', 'staff')
admin.site.register(models.User, UserAdmin)