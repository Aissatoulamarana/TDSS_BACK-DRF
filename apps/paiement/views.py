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
def add_payment_view(request):
    default_devise = Devise.objects.first()
    initial_value = {'devise': default_devise}
    context_empty = {
        'paymentform': PaymentForm(prefix= "payment", initial= initial_value), 
        'payerform': PayerForm(prefix= "payer"),
        'segment': 'paiements'
    }

    if request.method == "POST":

        paymentform = PaymentForm(request.POST, prefix= "payment")
        payerform = PayerForm(request.POST, prefix= "payer")

        paymentform.fields["payer"].required = False
        
        if paymentform.is_valid() and payerform.is_valid():
            print("Valid forms submitted!")

            new_payer = payerform.save(commit=False)

            new_payer.save()
            print("Payer created!")

            new_payment = paymentform.save(commit=False)
            new_payment.payer = new_payer
            new_payment.created_by = request.user

            new_payment.save()
            print("Payment created!")

            messages.success(request, "Nouveau paiement ajouté.")
            return redirect("paiement:payments")
        else:
            context = {
                'paymentform': paymentform, 
                'payerform': payerform, 
                'ErrorMessage': "Formulaire invalid soumit",
                'segment': 'paiements'
            }
            return render(request, "paiements/add-payment.html", context)
        
    return render(request, "paiements/add-payment.html", context_empty)



@login_required(login_url="/login/")
def devises_view(request):
    devises = Devise.objects.all()

    return render(request, "paiements/devises.html", {
        'devises': devises,
        'segment': "paiements"
    })
