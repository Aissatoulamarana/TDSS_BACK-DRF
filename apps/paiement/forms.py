# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import forms
from django.forms import (
    TextInput,
    NumberInput,
    Select,
    Textarea,
    FileInput,
    DateTimeInput,
    DateInput,
    EmailInput,
    RadioSelect,
    TimeInput,
    ClearableFileInput,
)
from .models import (
    Devise,
    Facture,
    Job,
    JobCategory,
    Payer,
    Payment,
    Employee,
    Declaration,
)

# My forms here


class DeviseForm(forms.ModelForm):
    class Meta:
        model = Devise
        fields = ("name", "sign", "value", "comment")
        # Omitted fields: id
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom de la devise",
                    "autofocus": True,
                }
            ),
            "sign": TextInput(
                attrs={"class": "form-control", "placeholder": "symbole"}
            ),
            "value": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "type": "amount",
                    "min": 0,
                }
            ),
            "comment": Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Commentaire...",
                    "class": "form-control",
                }
            ),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            "job_category",
            "job",
            "passport_number",
            "first",
            "last",
            "email",
            "phone",
        )
        # Omitted fields: id, declaration,
        widgets = {
            "job_category": Select(
                attrs={"class": "form-control", "placeholder": "Catégorie"}
            ),
            "job": Select(attrs={"class": "form-control", "placeholder": "Fonction"}),
            "passport_number": TextInput(
                attrs={"class": "form-control", "placeholder": "N° de psseport"}
            ),
            "first": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Prénoms",
                    "autofocus": True,
                }
            ),
            "last": TextInput(attrs={"class": "form-control", "placeholder": "Nom"}),
            "email": EmailInput(
                attrs={"class": "form-control", "placeholder": "example@mail.com"}
            ),
            "phone": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "N° de téléphone",
                    "min": 0,
                    "type": "phone",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields["job_category"].empty_label = "Sélectionner la catégorie"
        self.fields["job"].empty_label = "Sélectionner la fonction"
        self.fields["job"].queryset = Job.objects.order_by("name").all()
        self.fields["job_category"].queryset = JobCategory.objects.order_by(
            "name"
        ).all()


class DeclarationForm(forms.ModelForm):
    class Meta:
        model = Declaration
        fields = ("title", "comment")
        # Omitted fields: id, reference, total_employee, created_by, created_on, modified_on
        widgets = {
            "title": TextInput(attrs={"class": "form-control", "placeholder": "Titre"}),
            "comment": Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Commentaire...",
                    "class": "form-control",
                }
            ),
        }


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ("client", "amount", "devise", "comment")
        # Omitted fields: id, reference, created_by, created_on, modified_on
        widgets = {
            "client": Select(attrs={"class": "form-control"}),
            "amount": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "min": 0,
                    "type": "number",
                }
            ),
            "devise": Select(attrs={"class": "form-control"}),
            "comment": Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Commentaire...",
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        self.fields["client"].empty_label = "Sélectionner la société"


class PayerForm(forms.ModelForm):
    class Meta:
        model = Payer
        fields = (
            "first",
            "last",
            "email",
            "phone",
            "country_origin",
            "employer",
            "job",
            "address",
        )
        # Omitted fields: id
        widgets = {
            "first": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Prénoms",
                    "autofocus": True,
                }
            ),
            "last": TextInput(attrs={"class": "form-control", "placeholder": "Nom"}),
            "email": EmailInput(
                attrs={"class": "form-control", "placeholder": "example@mail.com"}
            ),
            "phone": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "N° de téléphone",
                    "min": 0,
                    "type": "phone",
                }
            ),
            "country_origin": Select(
                attrs={"class": "form-control", "placeholder": "Nationalité"}
            ),
            "employer": Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sélectionner l'employeur",
                }
            ),
            "job": Select(attrs={"class": "form-control", "placeholder": "Fonction"}),
            "address": Textarea(
                attrs={"rows": 3, "placeholder": "Adresse...", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PayerForm, self).__init__(*args, **kwargs)
        self.fields["country_origin"].empty_label = "Sélectionner le pays"
        self.fields["employer"].empty_label = "Sélectionner l'employeur"
        self.fields["job"].empty_label = "Sélectionner la fonction"


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("type", "amount", "devise", "comment")
        # Omitted fields: id, type, facture_ref, reference, payer, created_by, created_on, modified_on
        widgets = {
            "amount": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "min": 0,
                    "type": "number",
                    "readonly": True,
                }
            ),
            "devise": Select(attrs={"class": "form-control amount-param"}),
            "comment": Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Commentaire...",
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields["type"].empty_label = "Sélectionner le type de permis"
        self.fields["devise"].empty_label = None
        # self.fields['amount'].required = False


class EmployeeRenewForm(forms.Form):
    passport_number = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=TextInput(
            attrs={"class": "form-control", "placeholder": "N° de psseport"}
        ),
    )
