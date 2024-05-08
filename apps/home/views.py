# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Sum

from apps.authentication.models import CustomUser, Profile, ProfileType
from apps.authentication.forms import CustomUserForm, Agency, Region
from apps.paiement.models import Declaration, Facture, Payment, Devise, Employee

# Global devises for all views
devises = Devise.objects.all().order_by('id')

@login_required(login_url="/login/")
def index(request):

    if request.user.profile.type.uid == 1 or request.user.profile.type.uid == 3:
        context = {
            'segment': 'index',
            'taux': devises,
            'total_users': CustomUser.objects.all(),
            'total_profiles': Profile.objects.all(),
            'total_agencies': Agency.objects.all(),
            'agencies_conakry': Agency.objects.filter(region=Region.objects.get(code='GN-C')),
            'agencies_interior': Agency.objects.exclude(region=Region.objects.get(code='GN-C')),

            'total_declarations': Declaration.objects.all(),
            'total_employees': Employee.objects.all(),
            'total_factures': Facture.objects.all(),
            'total_paiements': Payment.objects.all(),
            'paiement_GNF': Payment.objects.filter(devise=Devise.objects.get(pk=1)).aggregate(Sum('amount'))['amount__sum'],
            'paiement_USD': Payment.objects.filter(devise=Devise.objects.get(pk=2)).aggregate(Sum('amount'))['amount__sum']
        }
    else:
        if request.user.type.uid == 1 or request.user.type.uid == 3:
            context = {
                'segment': 'index',
                'taux': devises,
                'total_users': CustomUser.objects.filter(created_by__profile=request.user.profile).order_by('-created_on'),
                'total_profiles': Profile.objects.all().order_by('-created_on'),
                'total_agencies': Agency.objects.filter(created_by__profile=Profile.objects.first()),
                'agencies_conakry': Agency.objects.filter(region=Region.objects.get(code='GN-C'), created_by__profile=request.user.profile),
                'agencies_interior': Agency.objects.exclude(region=Region.objects.get(code='GN-C')).filter(created_by__profile=request.user.profile),

                'total_declarations': Declaration.objects.filter(created_by__profile=request.user.profile).order_by('-created_on'),
                'total_employees': Employee.objects.filter(declaration__created_by__profile=request.user.profile),
                'total_factures': Facture.objects.filter(created_by__profile=request.user.profile).order_by('-created_on'),
                'total_paiements': Payment.objects.filter(created_by__profile=request.user.profile).order_by('-created_on'),
                'paiement_GNF': Payment.objects.filter(devise=Devise.objects.get(pk=1), created_by__profile=request.user.profile).aggregate(Sum('amount'))['amount__sum'],
                'paiement_USD': Payment.objects.filter(devise=Devise.objects.get(pk=2), created_by__profile=request.user.profile).aggregate(Sum('amount'))['amount__sum']
            }
        else:
            context = {
                'segment': 'index',
                'taux': devises,
                'total_users': CustomUser.objects.filter(created_by=request.user).order_by('-created_on'),
                'total_profiles': Profile.objects.all().order_by('-created_on'),
                'total_agencies': Agency.objects.filter(created_by=request.user),
                'agencies_conakry': Agency.objects.filter(region=Region.objects.get(code='GN-C'), created_by=request.user),
                'agencies_interior': Agency.objects.exclude(region=Region.objects.get(code='GN-C')).filter(created_by=request.user),

                'total_declarations': Declaration.objects.filter(created_by=request.user).order_by('-created_on'),
                'total_employees': Employee.objects.filter(declaration__created_by=request.user),
                'total_factures': Facture.objects.filter(created_by=request.user).order_by('-created_on'),
                'total_paiements': Payment.objects.filter(created_by=request.user).order_by('-created_on'),
                'paiement_GNF': Payment.objects.filter(devise=Devise.objects.get(pk=1), created_by=request.user).aggregate(Sum('amount'))['amount__sum'],
                'paiement_USD': Payment.objects.filter(devise=Devise.objects.get(pk=2), created_by=request.user).aggregate(Sum('amount'))['amount__sum']
            }

    # context = {
    #     'segment': 'index',
    #     'total_users': CustomUser.objects.all(),
    #     'total_profiles': Profile.objects.all(),
    #     'total_agencies': Agency.objects.all(),
    #     'agencies_conakry': Agency.objects.filter(region=Region.objects.get(code='GN-C')),
    #     'agencies_interior': Agency.objects.exclude(region=Region.objects.get(code='GN-C')),

    #     'total_declarations': Declaration.objects.all(),
    #     'total_employees': Employee.objects.all(),
    #     'total_factures': Facture.objects.all(),
    #     'total_paiements': Payment.objects.all(),
    #     'paiement_GNF': Payment.objects.filter(devise=Devise.objects.get(pk=1)).aggregate(Sum('amount'))['amount__sum'],
    #     'paiement_USD': Payment.objects.filter(devise=Devise.objects.get(pk=2)).aggregate(Sum('amount'))['amount__sum']
    # }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def graphs_view(request):
    context = {'segment': 'index', 'taux': devises,}

    html_template = loader.get_template('home/graphs.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def page_profile_view(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    context = {'userform': CustomUserForm(instance=user), 'user_id': user_id, 'segment': 'index', 'taux': devises}

    html_template = loader.get_template('home/page-profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def edit_page_profile_view(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    context_empty = {'userform': CustomUserForm(instance=user), 'user_id': user_id, 'segment': 'index', 'taux': devises}
    print(user.permissions)

    if request.method == "POST":
        
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            updated_user.username = updated_user.email

            updated_user.save()
            print("User updated!")

            messages.success(request, "Compte utilisateur modifié.")
            return redirect("home:page_profile", user_id= request.user.id)

        else:
            messages.error(request, "Formulaire invalid soumit.")
            return redirect("home:page_profile", user_id= request.user.id)

    return render(request, "home/page-profile.html", context_empty)



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
