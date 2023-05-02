# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from apps.authentication.models import CustomUser, Profile, ProfileType
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
