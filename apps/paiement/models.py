# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

import uuid
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


class Permit(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=30, choices=[('A', "A"), ('B', "B"), ('C', "C")], default="A")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    devise = models.ForeignKey(Devise, on_delete=models.PROTECT)
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=50)
    permit = models.ForeignKey(Permit, on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=[('ON', "Actif"), ('OFF', "Inactif")], default="ON")
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50)
    comment = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Declaration(models.Model):
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=[('unvalidated', "Non Validée"), ('validated', "Validée")], default="unvalidated")
    comment = models.TextField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Employee(models.Model):
    declaration = models.ForeignKey(Declaration, on_delete=models.PROTECT, related_name="employee_declarations")
    passport_number = models.CharField(max_length=50, unique=True)
    first = models.CharField(max_length=100, verbose_name="first name")
    last = models.CharField(max_length=50, verbose_name="last_name")
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.IntegerField()
    job_category = models.ForeignKey(JobCategory, on_delete=models.PROTECT, blank=True, null=True, related_name="employee_job_categories")
    job = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True, null=True, related_name="employee_jobs")

    def __str__(self):
        return f"{self.first} {self.last}"


class Facture(models.Model):
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(Profile, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    devise = models.ForeignKey(Devise, on_delete=models.PROTECT, related_name="facture_devises")
    comment = models.TextField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} | {self.amount} | {self.devise}"


class Payer(models.Model):
    first = models.CharField(max_length=100, verbose_name="first name")
    last = models.CharField(max_length=50, verbose_name="last_name")
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.IntegerField()
    country_origin = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True, related_name="payer_countries")
    employer = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True, null=True, related_name="payer_jobs")
    address = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first} {self.last}"


class Payment(models.Model):
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    facture_ref = models.ForeignKey(Facture, on_delete=models.PROTECT, blank=True, null=True)
    type = models.ForeignKey(Permit, on_delete=models.PROTECT, related_name="payment_permits_types")
    payer = models.ForeignKey(Payer, on_delete=models.PROTECT, related_name="payment_payers")
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    devise = models.ForeignKey(Devise, on_delete=models.PROTECT, related_name="payment_devises")
    comment = models.TextField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} | {self.amount} | {self.devise}"