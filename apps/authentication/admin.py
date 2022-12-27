# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, UserType, ProfileType, Profile, Region, Agency

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'created_on', 'modified_on')

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'status', 'comment')

class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'status', 'comment')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'type', 'account', 'status', 'picture', 'created_by', 'created_on', 'modified_on')

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(ProfileType, ProfileTypeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Agency, AgencyAdmin)

admin.site.unregister(Group)