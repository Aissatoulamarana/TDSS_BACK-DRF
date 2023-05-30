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

from apps.authentication.models import CustomUser, Profile, ProfileType
from apps.authentication.forms import CustomUserForm
from apps.paiement.models import Declaration, Facture, Payment


@login_required(login_url="/login/")
def index(request):
    context = {
        'segment': 'index',
        'total_users': CustomUser.objects.all().count(),
        'total_ministeres': Profile.objects.filter(type=ProfileType.objects.get(uid=3)).count(),
        'total_banques': Profile.objects.filter(type=ProfileType.objects.get(uid=2)).count(),
        'total_entreprise': Profile.objects.filter(type=ProfileType.objects.get(uid=4)).count(),

        'total_declarations': Declaration.objects.all().count(),
        'total_factures': Facture.objects.all().count(),
        'total_paiements': Payment.objects.all().count()
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def graphs_view(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/graphs.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def page_profile_view(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    context = {'userform': CustomUserForm(instance=user), 'user_id': user_id, 'segment': 'index'}

    html_template = loader.get_template('home/page-profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def edit_page_profile_view(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    context_empty = {'userform': CustomUserForm(instance=user), 'user_id': user_id, 'segment': 'index'}
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
