# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import template
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Devise, Facture, Payer, Payment
from .forms import DeviseForm, FactureForm, PayerForm, PaymentForm


@login_required(login_url="/login/")
def payments_view(request):
    payments = Payment.objects.all()
    form = PaymentForm()
    payerform = PayerForm()

    return render(request, "paiements/payments.html", {
        #  To edit
        'form': form,
        'payerform': payerform,
        'payments': payments,
        'segment': "paiements"
    })


@login_required(login_url="/login/")
def devises_view(request):
    devises = Devise.objects.all()

    return render(request, "paiements/devises.html", {
        'devises': devises,
        'segment': "paiements"
    })
