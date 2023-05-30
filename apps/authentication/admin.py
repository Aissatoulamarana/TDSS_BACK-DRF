# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, UserType, ProfileType, Profile, Region, Agency, Menu, SubMenu, Action, Permission

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'profile', 'first_name', 'last_name', 'created_on', 'modified_on')

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'status', 'comment')

class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'status', 'comment')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'type', 'status', 'picture', 'created_on', 'modified_on')

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'status')

class SubMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'menu_id', 'name', 'status')

class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'submenu_id', 'name', 'status')

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'profile_type', 'codes', 'list')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(ProfileType, ProfileTypeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(SubMenu, SubMenuAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Permission, PermissionAdmin)

admin.site.unregister(Group)