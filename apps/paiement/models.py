# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django.db import models
from apps.authentication.models import CustomUser, Profile

# Create your models here.

class Devise(models.Model):
    name = models.CharField(max_length=20)
    sign = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=7, decimal_places=2, default=1)
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Facture(models.Model):
    ref = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    devise = models.ForeignKey(Devise, on_delete=models.PROTECT, related_name="facture_devises")
    comment = models.TextField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ref} | {self.amount} | {self.devise}"


class Payer(models.Model):
    first = models.CharField(max_length=100, verbose_name="first name")
    last = models.CharField(max_length=50, verbose_name="last_name")
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.IntegerField()
    country_origin = models.CharField(max_length=100, blank=True, null=True)
    employer = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True)
    job = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first} {self.last}"


class Payment(models.Model):
    ref = models.DateTimeField(auto_now_add=True, editable=False)
    facture_ref = models.ForeignKey(Facture, on_delete=models.PROTECT, blank=True, null=True)
    type = models.CharField(max_length=50)
    payer = models.ForeignKey(Payer, on_delete=models.PROTECT, related_name="payment_payers")
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    devise = models.ForeignKey(Devise, on_delete=models.PROTECT, related_name="payment_devises")
    comment = models.TextField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ref} | {self.amount} | {self.devise}"