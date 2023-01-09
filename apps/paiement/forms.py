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
