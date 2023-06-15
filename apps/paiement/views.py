# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from uuid import UUID
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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter, A4

import qrcode


from .models import Devise, Facture, Payer, Payment, Permit, Employee, Declaration, JobCategory, Job
from apps.authentication.models import Profile, CustomUser
from .forms import DeviseForm, FactureForm, PayerForm, PaymentForm, EmployeeForm, DeclarationForm


@login_required(login_url="/login/")
def payments_view(request):
    if request.user.profile.type.uid == 1 or request.user.type.uid == 5:
        payments = Payment.objects.all().order_by('-modified_on')
    elif request.user.type.uid == 2:
        payments = Payment.objects.filter(created_by=request.user).order_by('-created_on')
    else:
        payments = Payment.objects.filter(created_by__profile=request.user.profile)
    
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
def generate_payment_view(request):
    context_empty = {
        'segment': 'paiements'
    }

    if request.method == "POST" and 'facture_ref' in request.POST:
        facture_ref = request.POST["facture_ref"]
        # print(facture_ref)

        try:
            facture = Facture.objects.get(reference=UUID(facture_ref).hex)

            default_devise = Devise.objects.first()
            initial_value = {'devise': default_devise}
            context_empty = {
                'paymentform': PaymentForm(prefix= "payment", initial= initial_value), 
                'payerform': PayerForm(prefix= "payer"),
                'facture': facture,
                'segment': 'paiements'
            }
            return render(request, "paiements/generate-payment.html", context_empty)
        except ValueError:
            messages.error(request, "Cette référence n'est pas valide.")
            return redirect("paiement:payments")
        except Facture.DoesNotExist:
            messages.error(request, "Cette facture n'existe pas.")
            return redirect("paiement:payments")
        
    elif request.method == "POST" and 'generate-form-submit' in request.POST:

        bill = request.POST.get('facture')
        facture = Facture.objects.get(reference=UUID(bill).hex)
        # print(facture.reference)
        
        paymentform = PaymentForm(request.POST, prefix= "payment")
        payerform = PayerForm(request.POST, prefix= "payer")

        # paymentform.fields["type"].required = False
        
        if paymentform.is_valid() and payerform.is_valid():
            # print("Valid forms submitted!")

            new_payer = payerform.save(commit=False)
            new_payer.employer = facture.client

            new_payer.save()
            # print("Payer created!")

            new_payment = paymentform.save(commit=False)
            new_payment.facture_ref = facture
            new_payment.payer = new_payer
            new_payment.created_by = request.user

            new_payment.save()
            # print("Payment created!")

            facture.status = 'paid'
            facture.save()

            messages.success(request, "Nouveau paiement ajouté.")
            return redirect("paiement:payments")
        else:
            context = {
                'paymentform': paymentform, 
                'payerform': payerform,
                'facture': facture,
                'ErrorMessage': "Formulaire invalid soumit",
                'segment': 'paiements'
            }
            return render(request, "paiements/generate-payment.html", context)


    # return redirect("paiement:payments")


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
        return JsonResponse({"error": "Erreur requête. Contactez l'admin."})


def get_devise(request, devise_id):
    if request.method == "GET":
        
        try:
            devise = Devise.objects.get(pk=devise_id)
        except Devise.DoesNotExist:
            return JsonResponse({'error': "Devise inexistante."})
        
        return JsonResponse({'devise_value': devise.value})
    else:
        return JsonResponse({"error": "Erreur requête. Contactez l'admin."})


@login_required(login_url="/login/")
def declarations_view(request):
    if request.user.profile.type.uid == 1 or request.user.type.uid == 5:
        declarations = Declaration.objects.all().order_by('-modified_on')
    elif request.user.type.uid == 4:
        declarations = Declaration.objects.filter(status='submitted').order_by('created_on')
    elif request.user.type.uid == 2:
        declarations = Declaration.objects.filter(created_by=request.user).order_by('-created_on')
    else:
        declarations = Declaration.objects.filter(created_by__profile=request.user.profile)
    
    form = DeclarationForm()

    return render(request, "paiements/declarations.html", {
        'declarationform': form,
        'declarations': declarations,
        'segment': "facturation"
    })


@login_required(login_url="/login/")
def add_declaration_view(request):
    context_empty = {
        'declarationform': DeclarationForm(),
        'declarations': Declaration.objects.all(),
        'segment': 'facturation'
    }

    if request.method == "POST":

        declarationform = DeclarationForm(request.POST)
        
        if declarationform.is_valid():
            # print("Valid forms submitted!")

            new_declaration = declarationform.save(commit=False)

            new_declaration.created_by = request.user

            new_declaration.save()

            messages.success(request, "Nouvelle déclaration ajoutée.")
            return redirect("paiement:declarations")
        else:
            context = {
                'declarationform': declarationform,
                'ErrorMessage': "Formulaire invalid soumit",
                'segment': 'Facturation'
            }
            return render(request, "paiements/declarations.html", context)
        
    return render(request, "paiements/declarations.html", context_empty)


@login_required(login_url="/login/")
def edit_declaration_view(request, declaration_id):
    try:
        declaration = Declaration.objects.get(pk=declaration_id)
    except Declaration.DoesNotExist:
        messages.error(request, "Déclaration inexistante.")
        return redirect("paiement:declarations")
    
    employees = Employee.objects.filter(declaration=declaration)
    context_empty = {
        'declarationform': DeclarationForm(instance=declaration, prefix= "declaration"),
        'employeeform': EmployeeForm(prefix= "employee"),
        'declaration_id': declaration_id,
        'employees': employees,
        'segment': 'facturation'
    }

    if request.method == "POST" and 'declaration-form-submit' in request.POST:
        
        declarationform = DeclarationForm(request.POST, instance=declaration, prefix= "declaration")
        if declarationform.is_valid():
            
            # print("Update form submited !")
            declaration_updated = declarationform.save()
            
            declaration_updated.save()

            messages.success(request, "Déclaration modifiée.")
            return redirect("paiement:declarations")
        else:
            context = {
                'declarationform': declarationform,
                'employeeform': EmployeeForm(prefix= "employee"),
                'declaration_id': declaration_id,
                'employees': employees,
                'segment': 'facturation',
                'ErrorMessage': "Formulaire invalid soumit."
            }
            return render(request, "paiements/edit-declaration.html", context)

    elif request.method == "POST" and 'employee-form-submit' in request.POST:
        # print("add employee form submitted")
        employeeform = EmployeeForm(request.POST, prefix="employee")
        if employeeform.is_valid():
            new_employee = employeeform.save(commit=False)
            new_employee.declaration = declaration

            new_employee.save()
            messages.success(request, "Employé ajouté.")
        else:
            print("Invalid form submitted")
            context_empty["ErrorMessage"] = "Formulaire invalid soumit."
    
    elif request.method == "POST" and 'delete-employee-form-submit' in request.POST:
        employee_id = request.POST["employee-id"]
        # print(f"Employee with id:{employee_id} is submitted for delete")
        try:
            employee = Employee.objects.get(pk=employee_id)
            employee.delete()
            messages.success(request, "Employé supprimé.")
        except Employee.DoesNotExist:
            messages.error(request, "Employé inexistant.")


    return render(request, "paiements/edit-declaration.html", context_empty)


@login_required(login_url="/login/")
def submit_declaration_view(request, declaration_id):
    
    try:
        declaration = Declaration.objects.get(pk=declaration_id)
        declaration.status = 'submitted'
        declaration.save()
        messages.success(request, "Déclaration soumise.")
    except Declaration.DoesNotExist:
        messages.error(request, "Déclaration inexistante.")
    
    return redirect("paiement:declarations")


@login_required(login_url="/login/")
def reject_declaration_view(request, declaration_id):
    reject_reason = request.POST["reject_reason"]
    if not reject_reason:
        messages.error(request, "Le motif de rejet est obligatoire.")
    else:
        # print(reject_reason)
    
        try:
            declaration = Declaration.objects.get(pk=declaration_id)
            declaration.status = 'rejected'
            declaration.reject_reason = reject_reason
            declaration.save()
            messages.success(request, "Déclaration rejetée.")
        except Declaration.DoesNotExist:
            messages.error(request, "Déclaration inexistante.")
    
    return redirect("paiement:declarations")


@login_required(login_url="/login/")
def validate_declaration_view(request, declaration_id):
    
    try:
        declaration = Declaration.objects.get(pk=declaration_id)
        declaration.status = 'validated'
        declaration.save()
        messages.success(request, "Déclaration validée.")
    except Declaration.DoesNotExist:
        messages.error(request, "Déclaration inexistante.")
    
    return redirect("paiement:declarations")


@login_required(login_url="/login/")
def bill_declaration_view(request, declaration_id):
    try:
        declaration = Declaration.objects.get(pk=declaration_id)
        # Getting job categories
        cadres = JobCategory.objects.get(pk=1)
        agents = JobCategory.objects.get(pk=2)
        ouvriers = JobCategory.objects.get(pk=3)

        new_bill = Facture()
        new_bill.declaration_ref = declaration
        new_bill.client = declaration.created_by.profile
        new_bill.total_cadres = declaration.employee_declarations.filter(job_category=cadres).count()
        new_bill.total_agents = declaration.employee_declarations.filter(job_category=agents).count()
        new_bill.total_ouvriers = declaration.employee_declarations.filter(job_category=ouvriers).count()

        new_bill.amount = (new_bill.total_cadres * cadres.permit.price) + (new_bill.total_agents * agents.permit.price) + (
                            new_bill.total_ouvriers * ouvriers.permit.price)
        
        new_bill.devise = cadres.permit.devise
        new_bill.created_by = request.user
        # print(new_bill.client.name, new_bill.amount, new_bill.devise)

        new_bill.save()

        declaration.status = 'billed'
        declaration.save()

        messages.success(request, "Déclaration facturée.")
    except Declaration.DoesNotExist:
        messages.error(request, "Déclaration inexistante.")
    
    return redirect("paiement:declarations")


@login_required(login_url="/login/")
def factures_view(request):
    if request.user.profile.type.uid == 1 or request.user.type.uid == 5:
        factures = Facture.objects.all().order_by('-modified_on')
    elif request.user.type.uid == 2:
        factures = Facture.objects.filter(status='unpaid').order_by('-created_on')
    else:
        factures = Facture.objects.filter(created_by__profile=request.user.profile)
    
    job_categories = JobCategory.objects.all()
    form = FactureForm()

    return render(request, "paiements/factures.html", {
        #  To edit
        'form': form,
        'factures': factures,
        'job_categories': job_categories,
        'segment': "facturation"
    })


@login_required(login_url="/login/")
def add_facture_view(request):
    default_devise = Devise.objects.first()
    initial_value = {'devise': default_devise}
    context_empty = {
        'factureform': FactureForm(initial= initial_value),
        'permits': Permit.objects.all(),
        'segment': 'facturation'
    }

    if request.method == "POST":

        factureform = FactureForm(request.POST)
        
        if factureform.is_valid():
            # print("Valid forms submitted!")

            new_facture = factureform.save(commit=False)

            new_facture.created_by = request.user

            new_facture.save()
            # print("Facture created!")

            messages.success(request, "Nouvelle facture ajoutée.")
            return redirect("paiement:factures")
        else:
            context = {
                'factureform': factureform,
                'ErrorMessage': "Formulaire invalid soumit",
                'segment': 'facturation'
            }
            return render(request, "paiements/add-facture.html", context)
        
    return render(request, "paiements/add-facture.html", context_empty)

