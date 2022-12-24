# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="email address", max_length=100, unique=True)
    phone = models.IntegerField(unique=True)
    job = models.TextField(max_length=50, blank=True, null=True, verbose_name="poste")
    reset_pwd = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    # USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class ProfileType(models.Model):
    uid = models.SmallIntegerField(verbose_name="profile_uid", unique=True)
    name = models.CharField(verbose_name="type name", max_length=100)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name="profile name", max_length=100)
    type = models.ForeignKey(ProfileType, on_delete=models.PROTECT)
    description = models.TextField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact = models.IntegerField(blank=True, null=True)
    account = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="profile_account")
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")
    picture = models.ImageField(upload_to="staticfiles", blank=True, null=True, verbose_name="profile picture")
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="profile_creator")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uuid} | {self.type}"

