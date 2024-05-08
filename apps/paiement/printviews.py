import io
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Image, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import simpleSplit
from reportlab.graphics.shapes import Drawing, Line, String
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER,TA_LEFT,TA_RIGHT

import qrcode

from .models import Devise, Facture, Payer, Payment, Permit, Employee, Declaration, JobCategory, Job
from apps.authentication.models import Profile, CustomUser

from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from django.utils.dateformat import DateFormat

# Function to format number to amount
def to_amount(number):
    return "{:0,.0f}".format(number).replace(','," ")


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

    # Creating the pdf document
    pdf = SimpleDocTemplate(buffer, title="Déclarations", pagesize=A4, topMargin=0.5*inch)

    elements = []
    styles=getSampleStyleSheet()

    if client.picture:
        client_image = (client.picture.url)[1:]
    else:
        client_image = 'apps/static/assets/img/brand/logo.jpg'
    elements.append(Image(client_image, width=100, height=80, hAlign="LEFT"))

    date = DateFormat(declaration.created_on)

    styleSheet = getSampleStyleSheet()
    style_title = styleSheet['Heading1']
    style_title.fontSize = 20 
    # style_title.fontName = 'Helvetica-Bold'
    style_title.alignment=TA_CENTER

    style_data = styleSheet['Normal']
    style_data.fontSize = 11 
    # style_data.fontName = 'Helvetica'
    style_data.alignment=TA_LEFT

    style_sign = styleSheet['Normal']
    style_sign.fontSize = 14 
    # style_data.fontName = 'Helvetica'
    style_sign.alignment=TA_LEFT
    
    d = Drawing(500, 50)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, hAlign='CENTER'))
    elements.append(Paragraph(f"DECLARATION N° 00{declaration.id}/{date.format('Y')}", style_title))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, hAlign='CENTER'))

    elements.append(Paragraph("<br/><br/>"))
    d.add(String(10, 125, f"Titre :  {declaration.title}", fontSize=11, fontName='Helvetica', fillColor=colors.black))
    d.add(String(350, 125, f"Date : {date.format('d/m/Y')}", fontSize=11, fontName='Helvetica', fillColor=colors.black))

    d.add(String(10, 90, f" {client.name}", fontSize=11, fontName='Helvetica', fillColor=colors.black))
    d.add(String(10, 75, f" Tél : {to_amount(client.contact)}", fontSize=11, fontName='Helvetica', fillColor=colors.black))
    d.add(String(10, 60, f" {client.adresse}", fontSize=11, fontName='Helvetica', fillColor=colors.black))
    # elements.append(Paragraph(f" {client.name}"))

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
    
    elements.append(Image('staticfiles/declaration_qr.png', width=70, height=70, hAlign="RIGHT"))

    d.add(String(20, 10, f"LISTE DES EMPLOYES", fontSize=16, fontName='Helvetica', fillColor=colors.black))
    d.add(String(380, 10, f"Total : {employees.count()}", fontSize=12, fontName='Helvetica', fillColor=colors.black))
    # elements.append(Paragraph(f"LISTE DES EMPLOYES"))
    elements.append(d)
    

    data = [
        ['N°','N° de passeport', 'Prénoms & Nom', 'Catégorie', 'Fonction', 'Téléphone'],
    ]

    counter = 1
    for employee in employees:
        data.append([f"{counter}", employee.passport_number, f"{employee.first} {employee.last}", f"{employee.job_category}", f"{employee.job}", f"{to_amount(employee.phone)}"])
        counter +=1

    LIST_STYLE = TableStyle(
        [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
            # ('LINEBEFORE', (0,0), (-1,0), 1, colors.black),
            ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('FONTSIZE', (0,0), (-1,0), 12, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            # ('ALIGN', (1,1), (1,5), 'CENTER'),
        ]
    )

    # Configure table style and word wrap
    table_style = getSampleStyleSheet()
    table_style = table_style["BodyText"]
    # table_style.wordWrap = 'CJK'
    table_style.fontSize = 9
    data2 = [[Paragraph(cell, table_style) for cell in row] for row in data]

    # Manage table cols width. --default is 83
    design_width = (0.4*inch, 1.2*inch, 2.5*inch, 1.2*inch, 1.4*inch, 0.9*inch)

    table = Table(data2, colWidths=design_width, repeatRows=1, splitByRow=1, style=LIST_STYLE)

    elements.append(table)

    elements.append(Paragraph("<br/><br/>" + f"L'employeur", style_sign))


    pdf.build(elements)

    buffer.seek(0)

    return FileResponse(buffer, filename=f"recu_declaration_num{declaration.id}.pdf")


@login_required(login_url="/login/")
def declaration_receipt_view_real(request, declaration_id):
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
    pdf.setFontSize(11, leading=None)
    pdf.drawString(55, 700, f"Titre :  {declaration.title}")
    pdf.drawString(470, 700, f"Date : {date.format('d/m/Y')}")
    # pdf.drawString(60, 730, f"- Informations du client -")

    pdf.setFontSize(10, leading=None)
    # pdf.drawString(55, 680, f"Titre :  {declaration.title}")
    pdf.drawString(55, 670, f" {client.name}")
    pdf.drawString(55, 657, f" Tél : {to_amount(client.contact)}")
    pdf.drawString(55, 645, f" {client.adresse}")
    # pdf.drawString(55, 625, f" Total employées : {employees.count()}")

    cadres = JobCategory.objects.get(pk=1)
    agents = JobCategory.objects.get(pk=2)
    ouvriers = JobCategory.objects.get(pk=3)

    data = [
        ['N°','N° de passeport', 'Prénoms & Nom', 'Catégorie', 'Fonction', 'Téléphone'],
    ]

    counter = 1
    for employee in employees:
        data.append([f"{counter}", employee.passport_number, f"{employee.first} {employee.last}", f"{employee.job_category}", f"{employee.job}", f"{to_amount(employee.phone)}"])
        counter +=1

    LIST_STYLE = TableStyle(
        [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
            # ('LINEBEFORE', (0,0), (-1,0), 1, colors.black),
            ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('FONTSIZE', (0,0), (-1,0), 12, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            # ('ALIGN', (1,1), (1,5), 'CENTER'),
        ]
    )

    # Configure table style and word wrap
    table_style = getSampleStyleSheet()
    table_style = table_style["BodyText"]
    # table_style.wordWrap = 'CJK'
    table_style.fontSize = 9
    data2 = [[Paragraph(cell, table_style) for cell in row] for row in data]

    # Manage table cols width. --default is 83
    design_width = (0.4*inch, 1.2*inch, 2.5*inch, 1.2*inch, 1.4*inch, 0.9*inch)

    table = Table(data2, colWidths=design_width, repeatRows=1, splitByRow=1, style=LIST_STYLE)

    # table = simpleSplit(table, 'Helvetica', 9, 83)

    pdf.setFontSize(12)
    pdf.drawString(60, 600, f"LISTE DES EMPLOYES")
    pdf.drawString(480, 600, f"Total : {employees.count()}")

    pdf.setFontSize(8)
    table.wrapOn(pdf, 25, 500)
    # table.drawOn(pdf, 25, 580-table._height)
    table.drawOn(pdf, 25, 50-table._height)

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
    
    pdf.drawImage('staticfiles/declaration_qr.png', 470, 615, 80, 80, showBoundary=False)

    pdf.setFontSize(12, leading=None)
    pdf.drawString(70, 550-table._height, f"L'employeur")

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
    # pdf.drawImage('apps/static/assets/img/brand/logo.jpg', 60, 750, 100, 80, showBoundary=False)
    pdf.drawImage('apps/static/assets/img/bill/header_aguipee_tdss.png', 0, 730, A4[0], 100, showBoundary=False)
    pdf.drawImage('apps/static/assets/img/bill/footer_aguipee_tdss.png', 0, 0, A4[0], 75, showBoundary=False)
    pdf.drawImage('apps/static/assets/img/bill/conditions_banque.png', 55, 140, 320, 190, showBoundary=False)
    # pdf.line(50, 750, 550, 750)
    pdf.setFontSize(20, leading=None)
    pdf.drawString(220, 700, f"Facture N° 00{facture.id}/{date.format('Y')}")
    pdf.setFontSize(10, leading=None)
    pdf.setFillColor(colors.darkblue)
    pdf.drawString(55, 650, f"CLIENT")
    pdf.line(55, 647, 90, 647)
    pdf.setFillColor(colors.black)
    pdf.drawString(55, 630, f"{client.name}")
    pdf.drawString(55, 615, f"Tél : {to_amount(client.contact)}")
    pdf.drawString(55, 600, f"{client.adresse}")

    pdf.setFillColor(colors.darkred)
    pdf.drawString(410, 645, f"Date facture : ")
    pdf.drawString(410, 632, f"Déclaration N° : ")
    pdf.drawString(410, 619, f"Date déclaration : ")
    pdf.setFillColor(colors.black)
    pdf.drawString(495, 645, f"{date.format('d/m/Y')}")
    pdf.drawString(495, 632, f"00{facture.declaration_ref.id}/{DateFormat(facture.declaration_ref.created_on).format('Y')}")
    pdf.drawString(495, 619, f"{DateFormat(facture.declaration_ref.created_on).format('d/m/Y')}")

    cadres = JobCategory.objects.get(pk=1)
    agents = JobCategory.objects.get(pk=2)
    ouvriers = JobCategory.objects.get(pk=3)

    data = [
        ['Catégorie de permis', 'Quantité', 'Prix Unitaire', 'Total ligne'],
    ]

    if facture.total_cadres > 0:
        data.append([f"{cadres.name} ({cadres.permit.name})", facture.total_cadres, to_amount(cadres.permit.price), to_amount(facture.total_cadres * cadres.permit.price) + f" {cadres.permit.devise.sign}"])
    if facture.total_agents > 0:
        data.append([f"{agents.name} ({agents.permit.name})", facture.total_agents, to_amount(agents.permit.price), to_amount(facture.total_agents * agents.permit.price) + f" {agents.permit.devise.sign}"])
    if facture.total_ouvriers > 0:
        data.append([f"{ouvriers.name} ({ouvriers.permit.name})", facture.total_ouvriers, to_amount(ouvriers.permit.price), to_amount(facture.total_ouvriers * ouvriers.permit.price) + f" {ouvriers.permit.devise.sign}"])

    data.append([' ', ' ', 'TOTAL GENERAL', f"{to_amount(facture.amount)} {facture.devise.sign}"])

    LIST_STYLE = TableStyle(
        [
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            # ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 13, colors.red),
            ('TEXTCOLOR', (0,0), (-1,0), colors.darkred),
            ('LINEABOVE', (0,0), (-1,-2), 0.1, colors.grey),
            ('LINEABOVE', (0,1), (-1,1), 1.5, colors.black),
            
            ('LINEABOVE', (0,-1), (-1,-1), 0.1, colors.grey),
            ('BACKGROUND', (0,-1), (-1,-1), colors.Color(241/256, 234/256, 234/256)),
            ('FONTSIZE', (0,-1), (-1,-1), 14, colors.red),
            ('LINEBELOW', (0,-1), (-1,-1), 0.1, colors.grey),
            
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ]
    )
    
    # Manage table cols width. --default is 123
    design_width = (2.5*inch, 1.0*inch, 1.6*inch, 1.8*inch)

    table = Table(data, colWidths=design_width, rowHeights=0.4*inch, style=LIST_STYLE)

    table.wrapOn(pdf, 55, 550)
    table.drawOn(pdf, 55, 580-table._height)

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
    
    pdf.drawImage('staticfiles/bill_qr.png', 60, 350, 70, 70, showBoundary=False)

    pdf.setFontSize(14, leading=None)
    pdf.drawString(430, 370, f"La Direction")
    pdf.line(430, 367, 505, 367)

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
    pdf.drawImage(client_image, 60, 750, 90, 70, showBoundary=False)
    pdf.drawImage('apps/static/assets/img/brand/logo.jpg', 450, 750, 90, 70, showBoundary=False)

    date = DateFormat(payment.created_on)

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdf.setFont('Vera', 14)
    
    pdf.line(50, 750, 550, 750)
    pdf.drawString(200, 730, f"RECU DE PAIEMENT N° 00{payment.id}/{date.format('Y')}")
    pdf.line(50, 720, 550, 720)
    pdf.setFontSize(11, leading=None)
    pdf.drawString(55, 700, f"Facture N° : 00{payment.facture_ref.id}/{DateFormat(payment.facture_ref.created_on).format('Y')}")
    pdf.drawString(450, 700, f"Date: {date.format('d/m/Y')}")

    pdf.setFontSize(10, leading=None)
    # pdf.drawString(60, 730, f"- Informations du payeur -")
    # pdf.drawString(55, 680, f"Facture N° : {payment.facture_ref.reference}")
    pdf.drawString(55, 675, f"CLIENT : {payment.facture_ref.client.name}")
    pdf.drawString(55, 662, f"Tél : {to_amount(payment.facture_ref.client.contact)}")
    pdf.drawString(55, 650, f"{payment.facture_ref.client.adresse}")
    
    permit_types = ""
    if payment.facture_ref.total_cadres > 0:
        permit_types += f"{cadres.permit} ({payment.facture_ref.total_cadres})"
    if payment.facture_ref.total_agents > 0:
        permit_types += f"\n{agents.permit} ({payment.facture_ref.total_agents})"
    if payment.facture_ref.total_ouvriers > 0:
        permit_types += f"\n{ouvriers.permit} ({payment.facture_ref.total_ouvriers})"

    data = [
        ['Description', 'Types de permis', 'Montant'],
        # ['Frais d\'acquisition', f"{cadres.permit} ({payment.facture_ref.total_cadres})\n{agents.permit} ({payment.facture_ref.total_agents})\n{ouvriers.permit} ({payment.facture_ref.total_ouvriers})", to_amount(payment.amount) + f" {payment.devise.sign}"]
        ['Frais d\'acquisition', permit_types, to_amount(payment.amount) + f" {payment.devise.sign}"]
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
    table.drawOn(pdf, 55, 620-table._height)

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
    
    pdf.drawImage('staticfiles/payment_qr.png', 60, 480, 70, 70, showBoundary=False)

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdf.setFont('Vera', 12)
    pdf.line(300, 535, 555, 535)
    pdf.drawString(320, 515, f"TOTAL TTC")
    pdf.line(420, 510, 420, 530)
    pdf.drawString(430, 515, f"{to_amount(payment.amount)} {payment.devise.sign}")
    pdf.line(300, 505, 555, 505)

    pdf.setFontSize(9, leading=None)
    pdf.drawString(90, 470, f"Le Client")
    pdf.drawString(420, 470, f"La Banque")

    pdf.line(5, 410, 55, 410)
    pdf.line(60, 410, 110, 410)
    pdf.line(115, 410, 165, 410)
    pdf.line(170, 410, 220, 410)
    pdf.line(225, 410, 275, 410)
    pdf.line(280, 410, 330, 410)
    pdf.line(335, 410, 385, 410)
    pdf.line(390, 410, 440, 410)
    pdf.line(445, 410, 495, 410)
    pdf.line(500, 410, 550, 410)
    pdf.line(555, 410, 605, 410)

    # ---------- Second part of the page ------------
    pdf.drawImage(client_image, 60, 320, 90, 70, showBoundary=False)
    pdf.drawImage('apps/static/assets/img/brand/logo.jpg', 450, 320, 90, 70, showBoundary=False)

    pdf.line(50, 320, 550, 320)
    pdf.setFontSize(14, leading=None)
    pdf.drawString(200, 300, f"RECU DE PAIEMENT N° 00{payment.id}/{date.format('Y')}")
    pdf.line(50, 290, 550, 290)
    pdf.setFontSize(11, leading=None) #f"Facture N° 00{facture.id}/{date.format('Y')}"
    pdf.drawString(55, 270, f"Facture N° : 00{payment.facture_ref.id}/{DateFormat(payment.facture_ref.created_on).format('Y')}")
    pdf.drawString(450, 270, f"Date: {date.format('d/m/Y')}")

    pdf.setFontSize(10, leading=None)
    pdf.drawString(55, 245, f"CLIENT : {payment.facture_ref.client.name}")
    pdf.drawString(55, 232, f"Tél : {to_amount(payment.facture_ref.client.contact)}")
    pdf.drawString(55, 220, f"{payment.facture_ref.client.adresse}")

    table.drawOn(pdf, 55, 200-table._height)
    pdf.drawImage('staticfiles/payment_qr.png', 60, 60, 70, 70, showBoundary=False)
    pdf.setFont('Vera', 12)
    pdf.line(300, 115, 555, 115)
    pdf.drawString(320, 95, f"TOTAL TTC")
    pdf.line(420, 90, 420, 110)
    pdf.drawString(430, 95, f"{to_amount(payment.amount)} {payment.devise.sign}")
    pdf.line(300, 85, 555, 85)

    pdf.setFontSize(9, leading=None)
    pdf.drawString(90, 50, f"Le Client")
    pdf.drawString(420, 50, f"La Banque")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return FileResponse(buffer, filename=f"recu_paiement_num{payment.id}.pdf")
