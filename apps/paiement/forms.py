# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import forms
from django.forms import TextInput, NumberInput, Select, Textarea, FileInput, DateTimeInput, DateInput, EmailInput, RadioSelect, TimeInput, ClearableFileInput
from .models import Devise, Facture, Payer, Payment

# My forms here

class DeviseForm(forms.ModelForm):
    class Meta:
        model = Devise
        fields = ('name', 'sign', 'value', 'comment')
        # Omitted fields: id
        widgets = {
            'name': TextInput(attrs={'class': "form-control", 'placeholder': "Nom de la devise", 'autofocus': True}),
            'sign': TextInput(attrs={'class': "form-control", 'placeholder': "symbole"}),
            'value': NumberInput(attrs={'class': "form-control", 'placeholder': "0.00", 'type': "amount", 'min': 0}),
            'comment': Textarea(attrs={'rows':3, 'placeholder': "Commentaire...", 'class': "form-control" })
        }


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ('date', 'amount', 'devise', 'comment')
        # Omitted fields: id, ref, created_by, created_on, modified_on
        widgets = {
            'date': DateInput(attrs={'class': "form-control", 'placeholder': "JJ/MM/AAAA"}),
            'amount': NumberInput(attrs={'class': "form-control", 'placeholder': "0.00", 'min': 0, 'type': "number"}),
            'devise': Select(attrs={'class': "form-control"}),
            'comment': Textarea(attrs={'rows':3, 'placeholder': "Commentaire...", 'class': "form-control" })
        }


class PayerForm(forms.ModelForm):
    class Meta:
        model = Payer
        fields = ('first', 'last', 'email', 'phone', 'country_origin', 'employer', 'job')
        # Omitted fields: id
        widgets = {
            'first': TextInput(attrs={'class': "form-control", 'placeholder': "Prénoms", 'autofocus': True}),
            'last': TextInput(attrs={'class': "form-control", 'placeholder': "Nom"}),
            'email': EmailInput(attrs={'class': "form-control", 'placeholder': "example@mail.com"}),
            'phone': NumberInput(attrs={'class': "form-control", 'placeholder': "N° de téléphone", 'min': 0, 'type': "phone"}),
            'country_origin': TextInput(attrs={'class': "form-control", 'placeholder': "Nationalité"}),
            'employer': Select(attrs={'class': "form-control", 'placeholder': "Sélectionner l'employeur"}),
            'job': TextInput(attrs={'class': "form-control", 'placeholder': "Fonction"}),
        }
        def __init__(self, *args, **kwargs):
            super(PayerForm, self).__init__(*args, **kwargs)
            self.fields['employer'].empty_label = "Sélectionner l'employeur"
        

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('facture_ref', 'type', 'date', 'amount', 'devise', 'comment')
        # Omitted fields: id, ref, payer, created_by, created_on, modified_on
        widgets = {
            'facture_ref': Select(attrs={'class': "form-control", 'placeholder': "Sélectionner la facture"}),
            'type': TextInput(attrs={'class': "form-control", 'placeholder': "Type de document"}),
            'date': DateInput(attrs={'class': "form-control", 'placeholder': "JJ/MM/AAAA"}),
            'amount': NumberInput(attrs={'class': "form-control", 'placeholder': "0.00", 'min': 0, 'type': "number"}),
            'devise': Select(attrs={'class': "form-control"}),
            'comment': Textarea(attrs={'rows':3, 'placeholder': "Commentaire...", 'class': "form-control" })
        }
        def __init__(self, *args, **kwargs):
            super(PaymentForm, self).__init__(*args, **kwargs)
            self.fields['facture_ref'].empty_label = "Sélectionner la facture"
        