# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import template
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.template import loader
from django.urls import reverse
import json
import io
from reportlab.pdfgen import canvas
from reportlab.platypus import Table


from .models import Devise, Facture, Payer, Payment, Permit
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
        
        if paymentform.is_valid() and payerform.is_valid():
            # print("Valid forms submitted!")

            new_payer = payerform.save(commit=False)

            new_payer.save()
            # print("Payer created!")

            new_payment = paymentform.save(commit=False)
            new_payment.payer = new_payer
            new_payment.created_by = request.user

            new_payment.save()
            # print("Payment created!")

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
def edit_payment_view(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    payer = Payer.objects.get(pk=payment.payer.id)
    context_empty = {
        'paymentform': PaymentForm(instance=payment, prefix= "payment"),
        'payerform': PayerForm(instance=payer, prefix= "payer"),
        'payment_id': payment_id, 
        'segment': 'paiements'
    }

    if request.method == "POST":
        
        paymentform = PaymentForm(request.POST, instance=payment, prefix= "payment")
        payerform = PayerForm(request.POST, instance=payer, prefix= "payer")
        if paymentform.is_valid() and payerform.is_valid():
            
            # print("Update form submited !")
            payer_updated = payerform.save()
            payer_updated.save()
            payment_updated = paymentform.save(commit=False)
            payment_updated.payer = payer_updated
            payment_updated.save()

            messages.success(request, "Payment modifié avec succès.")
            return redirect("paiement:payments")
        else:
            context = {
                'paymentform': PaymentForm(instance=payment, prefix= "payment"),
                'payerform': PayerForm(instance=payer, prefix= "payer"),
                'ErrorMessage': "Formulaire invalid soumit.",
                'payment_id': payment_id, 
                'segment': 'paiements'
            }
            return render(request, "paiements/edit-payment.html", context)


    return render(request, "paiements/edit-payment.html", context_empty)


@login_required(login_url="/login/")
def payment_receipt_view(request, payment_id):
    # Getting the payment
    payment = Payment.objects.get(pk=payment_id)

    # Creating a buffer for the pdf
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.line(50,800, 550, 800)
    pdf.drawString(200, 780, f"RECU DE PAIEMENT N° 00{payment.id}/2023")
    pdf.line(50,770, 550, 770)
    pdf.setFontSize(8, leading=None)
    pdf.drawString(55, 750, f"Référence: {payment.reference}")
    pdf.drawString(400, 750, f"Date: {payment.created_on}")
    # pdf.drawString(60, 730, f"- Informations du payeur -")
    pdf.drawString(55, 720, f"Prénom & Nom:  {payment.payer.first} {payment.payer.last}")
    pdf.drawString(55, 710, f"Nationalité: {payment.payer.country_origin}")
    pdf.drawString(55, 700, f"Employeur: {payment.payer.employer}")
    pdf.drawString(55, 690, f"Fonction: {payment.payer.job}")
    pdf.drawString(55, 680, f"Téléphone: {payment.payer.phone}")

    data = [
        ['Description', 'Type de permis', 'Quantité', 'Montant'],
        ['Frais d\'acquisition', payment.type, '01', payment.amount]
    ]
    table = Table(data, colWidths=150)

    table.wrapOn(pdf, 55, 600)
    table.drawOn(pdf, 55, 600)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return FileResponse(buffer, filename="hello.pdf")


@login_required(login_url="/login/")
def devises_view(request):
    devises = Devise.objects.all()
    guinean_franc = Devise.objects.first()
    dollar = Devise.objects.get(pk=2)
    euro = Devise.objects.get(pk=3)

    return render(request, "paiements/devises.html", {
        'guinean_franc': guinean_franc,
        'dollar': dollar,
        'euro': euro,
        'devises': devises,
        'segment': "paiements"
    })


@login_required(login_url="/login/")
def devises_update_view(request):
    if request.method == "POST":
        new_gnf = request.POST["guinean_franc"]
        new_dollar = request.POST["dollar"]
        new_euro = request.POST["euro"]

        Devise.objects.filter(pk=1).update(value=new_gnf)
        Devise.objects.filter(pk=2).update(value=new_dollar)
        Devise.objects.filter(pk=3).update(value=new_euro)

        messages.success(request, "Dévises actualisé.")
        devises = Devise.objects.all()
        return render(request, "paiements/devises.html", {
            'guinean_franc': Devise.objects.first(),
            'dollar': Devise.objects.get(pk=2),
            'euro': Devise.objects.get(pk=3),
            'devises': devises,
            'segment': "paiements"
        })
    else:
        return redirect("paiement:payments")


def get_devise_value(request, permit_id, devise_id):
    if request.method == "GET":
        
        # data = json.loads(request.body)
        # permit_id = data["permit"]
        # Get permit price
        try:
            permit = Permit.objects.get(pk=permit_id)
        except Permit.DoesNotExist:
            return JsonResponse({'error': "Type de permis inexistant."})

        try:
            devise = Devise.objects.get(pk=devise_id)
        except Devise.DoesNotExist:
            return JsonResponse({'error': "Devise inexistante."})
        
        return JsonResponse({'permit_price': permit.price, 'devise_value': devise.value})
    else:
        return JsonResponse({"error": "Erreur requête. COntactez l'admin."})
