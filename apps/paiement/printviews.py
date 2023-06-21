import io
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

import qrcode

from .models import Devise, Facture, Payer, Payment, Permit, Employee, Declaration, JobCategory, Job
from apps.authentication.models import Profile, CustomUser

from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.utils.dateformat import DateFormat


@login_required(login_url="/login/")
def declaration_receipt_view(request, declaration_id):
    # Getting the payment
    try:
        declaration = Declaration.objects.get(pk=declaration_id)
    except Declaration.DoesNotExist:
        messages.error(request, "Déclaration inexistante.")
        return redirect("paiement:declarations")

    client = declaration.created_by.profile
    employees = Employee.objects.filter(declaration=declaration)
    
    # Creating a buffer for the pdf
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setPageSize(A4)
    width, height = A4
    pdf.setTitle("Déclarations")

    if client.picture:
        client_image = (client.picture.url)[1:]
    else:
        client_image = 'apps/static/assets/img/brand/logo.jpg'
    pdf.drawImage(client_image, 60, 750, 100, 80, showBoundary=False)

    date = DateFormat(declaration.created_on)
    
    pdf.line(50, 750, 550, 750)
    pdf.drawString(200, 730, f"DECLARATION N° 00{declaration.id}/{date.format('Y')}")
    pdf.line(50, 720, 550, 720)
    pdf.setFontSize(8, leading=None)
    pdf.drawString(55, 700, f"Référence: {declaration.reference}")
    
    pdf.drawString(480, 700, f"Date: {date.format('d/m/y')}")
    # pdf.drawString(60, 730, f"- Informations du client -")

    pdf.drawString(55, 680, f"Titre :  {declaration.title}")
    pdf.drawString(55, 670, f"Entreprise :  {client.name}")
    pdf.drawString(55, 660, f"Téléphone : {client.contact}")
    pdf.drawString(55, 650, f"Adresse : {client.adresse}")
    pdf.drawString(55, 640, f"Total employées : {employees.count()}")
    pdf.drawString(55, 630, f"")

    cadres = JobCategory.objects.get(pk=1)
    agents = JobCategory.objects.get(pk=2)
    ouvriers = JobCategory.objects.get(pk=3)

    data = [
        ['N°','N° de passeport', 'Prénoms & Nom', 'Fonction', 'Catégorie', 'Téléphone'],
    ]

    counter = 1
    for employee in employees:
        data.append([f"{counter}", employee.passport_number, f"{employee.first} {employee.last}", f"{employee.job}", f"{employee.job_category}", f"{employee.phone}"])
        counter +=1

    LIST_STYLE = TableStyle(
        [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
            # ('LINEBEFORE', (0,0), (-1,0), 1, colors.black),
            ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('FONTSIZE', (0,1), (-1,counter), 8, colors.black),
            ('FONTSIZE', (1,0), (0,-1), 10, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ]
    )

    # Configure table style and word wrap
    table_style = getSampleStyleSheet()
    table_style = table_style["BodyText"]
    table_style.wordWrap = 'CJK'
    data2 = [[Paragraph(cell, table_style) for cell in row] for row in data]

    # Manage table cols width. --default is 83
    design_width = (0.3*inch, 1.2*inch, 2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch)

    table = Table(data, colWidths=design_width, splitByRow=1, style=LIST_STYLE)

    pdf.setFontSize(12)
    pdf.drawString(60, 600, f"LISTE DES EMPLOYES")

    pdf.setFontSize(8)
    table.wrapOn(pdf, 25, 500)
    table.drawOn(pdf, 25, 580-table._height)

    # Creating the QR Code
    qr_data = {
        'ID': declaration.id, 
        'REF': declaration.reference, 
        'Client': client.name, 
        'Total Employés': employees.count()
    }
    qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('staticfiles/declaration_qr.png')
    
    pdf.drawImage('staticfiles/declaration_qr.png', 470, 610, 80, 80, showBoundary=False)

    # pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    # pdf.setFont('Vera', 10)
    # # pdf.line(300, 550, 550, 550)
    # pdf.drawString(430, 350, f"Signature")
    # pdf.drawString(430, 270, f"Nom, Prénom et fonction")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return FileResponse(buffer, filename=f"recu_declaration_num{declaration.id}.pdf")




@login_required(login_url="/login/")
def bill_receipt_view(request, bill_id):
    # Getting the payment
    try:
        facture = Facture.objects.get(pk=bill_id)
    except Payment.DoesNotExist:
        messages.error(request, "Facture inexistante.")
        return redirect("paiement:factures")
    
    client = facture.declaration_ref.created_by.profile
    
    date = DateFormat(facture.created_on)

    # Creating a buffer for the pdf
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setPageSize(A4)
    width, height = A4
    pdf.setTitle("Factures")
    pdf.drawImage('apps/static/assets/img/brand/logo.jpg', 60, 750, 100, 80, showBoundary=False)
    pdf.line(50, 750, 550, 750)
    pdf.drawString(220, 730, f"FACTURE N° 00{facture.id}/{date.format('Y')}")
    pdf.line(50, 720, 550, 720)
    pdf.setFontSize(8, leading=None)
    pdf.drawString(55, 700, f"Référence: {facture.reference}")
    
    pdf.drawString(480, 700, f"Date: {date.format('d/m/y')}")
    # pdf.drawString(60, 730, f"- Informations du client -")
    pdf.drawString(55, 680, f"Entreprise :  {client.name}")
    pdf.drawString(55, 670, f"Téléphone : {client.contact}")
    pdf.drawString(55, 660, f"Adresse : {client.adresse}")
    pdf.drawString(55, 650, f"")
    pdf.drawString(55, 640, f"")

    cadres = JobCategory.objects.get(pk=1)
    agents = JobCategory.objects.get(pk=2)
    ouvriers = JobCategory.objects.get(pk=3)

    data = [
        ['Catégorie de permis', 'Quantité', 'P.U', 'Montant'],
    ]

    if facture.total_cadres > 0:
        data.append(['Cadres', facture.total_cadres, cadres.permit.price, facture.total_cadres * cadres.permit.price])
    if facture.total_agents > 0:
        data.append(['Agent Administratif', facture.total_agents, agents.permit.price, facture.total_agents * agents.permit.price])
    if facture.total_ouvriers > 0:
        data.append(['Ouvriers', facture.total_ouvriers, ouvriers.permit.price, facture.total_ouvriers * ouvriers.permit.price])

    LIST_STYLE = TableStyle(
        [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
            # ('LINEBEFORE', (0,0), (-1,0), 1, colors.black),
            # ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('FONTSIZE', (0,1), (5,4), 9, colors.black),
            ('FONTSIZE', (0,0), (0,5), 11, colors.black),
            ('BACKGROUND', (0,0), (5,0), colors.lightgrey),
            ('ALIGN', (0,0), (3,0), 'CENTER'),
            ('ALIGN', (1,1), (3,3), 'CENTER'),
        ]
    )

    # Manage table cols width. --default is 123
    design_width = (2.5*inch, 1.0*inch, 1.6*inch, 1.8*inch)

    table = Table(data, colWidths=design_width, style=LIST_STYLE)

    table.wrapOn(pdf, 55, 550)
    table.drawOn(pdf, 55, 550)
    # table.drawOn(pdf, 25, 630-table._height)

    # Creating the QR Code
    qr_data = {
        'ID': facture.id, 
        'REF': facture.reference, 
        'Client': f"{client.name}", 
        'Montant': f"{facture.amount} {facture.devise.sign}"
    }
    qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('staticfiles/bill_qr.png')
    
    pdf.drawImage('staticfiles/bill_qr.png', 60, 450, 90, 90, showBoundary=False)

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdf.setFont('Vera', 12)
    pdf.line(310, 520, 540, 520)
    pdf.drawString(320, 500, f"TOTAL TTC")
    pdf.line(423, 495, 423, 515)
    pdf.drawString(450, 500, f"{facture.amount} {facture.devise.sign}")
    pdf.line(310, 490, 540, 490)

    # pdf.setFontSize(10)
    # pdf.drawString(400, 450, f"Signature")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return FileResponse(buffer, filename=f"recu_facture_num{facture.id}.pdf")



@login_required(login_url="/login/")
def payment_receipt_view(request, payment_id):
    # Getting the payment
    try:
        payment = Payment.objects.get(pk=payment_id)
    except Payment.DoesNotExist:
        messages.error(request, "Recu de paiement inexistant.")
        return redirect("paiement:payments")
    
    # Getting job categories
    cadres = JobCategory.objects.get(pk=1)
    agents = JobCategory.objects.get(pk=2)
    ouvriers = JobCategory.objects.get(pk=3)

    client = payment.created_by.profile

    # Creating a buffer for the pdf
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setPageSize(A4)
    width, height = A4
    pdf.setTitle("Paiements")

    if client.picture:
        client_image = (client.picture.url)[1:]
    else:
        client_image = 'apps/static/assets/img/brand/logo.jpg'
    pdf.drawImage(client_image, 60, 750, 100, 80, showBoundary=False)

    date = DateFormat(payment.created_on)
    
    pdf.line(50, 750, 550, 750)
    pdf.drawString(200, 730, f"RECU DE PAIEMENT N° 00{payment.id}/{date.format('Y')}")
    pdf.line(50, 720, 550, 720)
    pdf.setFontSize(8, leading=None)
    pdf.drawString(55, 700, f"Référence: {payment.reference}")

    pdf.drawString(480, 700, f"Date: {date.format('d/m/y')}")
    # pdf.drawString(60, 730, f"- Informations du payeur -")
    pdf.drawString(55, 680, f"Facture N° : {payment.facture_ref.reference}")
    pdf.drawString(55, 670, f"Entreprise : {payment.payer.employer}")
    pdf.drawString(55, 660, f"Payer Par :  {payment.payer.first} {payment.payer.last}")
    pdf.drawString(55, 650, f"Fonction: {payment.payer.job}")
    pdf.drawString(55, 640, f"Téléphone: {payment.payer.phone}")

    data = [
        ['Description', 'Types de permis', 'Montant'],
        ['Frais d\'acquisition', f"{cadres.permit} ({payment.facture_ref.total_cadres})\n{agents.permit} ({payment.facture_ref.total_agents})\n{ouvriers.permit} ({payment.facture_ref.total_ouvriers})", payment.amount]
    ]

    LIST_STYLE = TableStyle(
        [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
            # ('LINEBEFORE', (0,0), (-1,0), 1, colors.black),
            # ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('FONTSIZE', (1,0), (1,4), 9, colors.black),
            ('FONTSIZE', (0,0), (0,4), 11, colors.black),
            ('BACKGROUND', (0,0), (3,0), colors.lightgrey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('ALIGN', (1,1), (1,1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]
    )

    # Manage table cols width. --default is 123
    design_width = (2.5*inch, 2.56*inch, 1.9*inch)

    table = Table(data, colWidths=design_width, style=LIST_STYLE)

    table.wrapOn(pdf, 55, 560)
    table.drawOn(pdf, 55, 560)
    # table.drawOn(pdf, 25, 620-table._height)

    # Creating the QR Code
    qr_data = {
        'ID': payment.id, 
        'REF': payment.reference, 
        'Payeur': f"{payment.payer.first} {payment.payer.last}", 
        'Montant': f"{payment.amount} {payment.devise.sign}"
    }
    qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('staticfiles/payment_qr.png')
    
    pdf.drawImage('staticfiles/payment_qr.png', 60, 465, 90, 90, showBoundary=False)

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdf.setFont('Vera', 12)
    pdf.line(300, 535, 555, 535)
    pdf.drawString(320, 515, f"TOTAL TTC")
    pdf.line(420, 510, 420, 530)
    pdf.drawString(430, 515, f"{payment.amount} {payment.devise.sign}")
    pdf.line(300, 505, 555, 505)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return FileResponse(buffer, filename=f"recu_paiement_num{payment.id}.pdf")
