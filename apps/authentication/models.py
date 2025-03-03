# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.


class ProfileType(models.Model):
    ADMIN = 'admin'  # 1
    BANK = 'bank'   # 2
    ENTREPRISE = 'entreprise'  # 4
    MINISTRY = 'ministry'  # 3
    AGUIPE = 'aguipe'  # 5

    uid = models.SmallIntegerField(unique=True)
    code = models.CharField(verbose_name=_('Code'), max_length=30, unique=True, null=True)
    name = models.CharField(verbose_name="type name", max_length=100)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class UserType(models.Model):
    ADMIN = 'admin'  # 1
    AGENT = 'agent'  # 2
    SUPERVISOR = 'supervisor'  # 3
    AGUIPE = 'aguipe'  # 4
    TDSS = 'tdss'  # 5
    MINISTRY = 'ministry'  # 6

    uid = models.SmallIntegerField(unique=True)
    code = models.CharField(verbose_name=_('Code'), max_length=30, unique=True, null=True)
    name = models.CharField(verbose_name="type name", max_length=100)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    code = models.CharField(max_length=20, verbose_name="Code_region", unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Agency(models.Model):
    code = models.CharField(max_length=20, verbose_name="Code_agence", unique=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="region_agency")
    name = models.CharField(max_length=100)
    comment = models.TextField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, blank=True, null=True, related_name="agency_users")
    

    def __str__(self):
        return self.name
    

class Permission(models.Model):
    name = models.CharField(max_length=100)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.PROTECT, related_name="permissions_profile_types")
    codes = models.TextField(max_length=2048)
    list = models.TextField(max_length=2048)

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name="profile name", max_length=100)
    type = models.ForeignKey(ProfileType, on_delete=models.PROTECT)
    description = models.TextField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="profile_location", blank=True, null=True)
    contact = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")
    picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True, verbose_name="profile picture")
    email = models.EmailField(max_length=100, blank=True, null=True)
    adresse = models.TextField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="email address", max_length=100, unique=True)
    phone = models.IntegerField(unique=True , null=True, blank=True)
    type = models.ForeignKey(UserType, on_delete=models.PROTECT, null=True , blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True, related_name="user_profiles")
    job = models.TextField(max_length=50, blank=True, null=True, verbose_name="poste")
    location = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="user_location", blank=True, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT, related_name="user_agency", blank=True, null=True)
    picture = models.ImageField(upload_to="user_pictures", blank=True, null=True, verbose_name="user picture")
    reset_pwd = models.BooleanField(default=True)
    permissions = models.ForeignKey(Permission, on_delete=models.PROTECT, blank=True, null=True, related_name="customuser_permissions")
    created_by = models.ForeignKey('self', on_delete=models.PROTECT, related_name="user_creator", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    country = models.TextField(max_length=100, default='Guinea')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Menu(models.Model):
    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")

    def __str__(self):
        return f"{self.name}"


class SubMenu(models.Model):
    uid = models.CharField(max_length=50)
    menu_id = models.ForeignKey(Menu, on_delete=models.PROTECT, related_name="menu_subs")
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")

    def __str__(self):
        return f"{self.name}"


class Action(models.Model):
    uid = models.CharField(max_length=50)
    submenu_id = models.ForeignKey(SubMenu, on_delete=models.PROTECT, related_name="submenu_actions")
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")

    def __str__(self):
        return f"{self.name}"
