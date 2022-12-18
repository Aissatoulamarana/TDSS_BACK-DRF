# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, ProfileType, Profile

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'created_on', 'modified_on')

class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'status', 'comment')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'type', 'account', 'status', 'picture', 'created_by', 'created_on', 'modified_on')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProfileType, ProfileTypeAdmin)
admin.site.register(Profile, ProfileAdmin)

admin.site.unregister(Group)