import io
import xlsxwriter
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

from .models import Devise, Facture, Payer, Payment, Permit, Employee, Declaration, JobCategory, Job
from apps.authentication.models import Profile, CustomUser, Agency, Permission, ProfileType, UserType

from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count

from django.utils.dateformat import DateFormat
from datetime import datetime

# Function to format number to amount
def to_amount(number):
    return "{:0,.0f}".format(number).replace(','," ")


def export_pdf(name, data, design_width):
    
    # Creating a buffer for the pdf
    buffer = io.BytesIO()

    # Creating the pdf document
    pdf = SimpleDocTemplate(buffer, title=name, pagesize=A4, topMargin=0.1*inch)

    elements = []
    styles=getSampleStyleSheet()

    page_header = 'apps/static/assets/img/bill/header_aguipee_tdss.png'
    page_footer = 'apps/static/assets/img/bill/footer_aguipee_tdss.png'

    elements.append(Image(page_header, width=A4[0], height=100, hAlign="CENTER"))

    print_date = DateFormat(datetime.now())

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

    elements.append(Paragraph("<br/><br/>"))
    
    d = Drawing(500, 50)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, hAlign='CENTER'))
    elements.append(Paragraph(f"TABLEAU DES {name.upper()}", style_title))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, hAlign='CENTER'))

    elements.append(Paragraph("<br/><br/>"))
    # d.add(String(10, 125, f"Titre :  {name}", fontSize=11, fontName='Helvetica', fillColor=colors.black))
    d.add(String(320, 60, f"Date : {print_date.format('d/m/Y H:m')}", fontSize=11, fontName='Helvetica', fillColor=colors.black))


    d.add(String(20, 20, f"LISTE DES {name.upper()}", fontSize=16, fontName='Helvetica', fillColor=colors.black))
    elements.append(d)

    LIST_STYLE = TableStyle(
        [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
            ('LINEABOVE', (0,0), (-1,-1), 1, colors.black),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('FONTSIZE', (0,0), (-1,0), 12, colors.black),
            # ('FONTSIZE', (1,0), (-1,-1), 9, colors.red),
            ('BACKGROUND', (0,0), (-1,0), colors.orange),
        ]
    )

    # Configure table style and word wrap
    table_style = getSampleStyleSheet()
    table_style = table_style["BodyText"]
    table_style.fontSize = 9
    data2 = [[Paragraph(cell, table_style) for cell in row] for row in data]

    table = Table(data2, colWidths=design_width, repeatRows=1, splitByRow=1, style=LIST_STYLE)

    elements.append(table)

    pdf.build(elements)

    buffer.seek(0)

    return buffer


@login_required(login_url="/login/")
def exportpdf_agencies_view(request):
    name = "Agences"
    agencies = Agency.objects.all().order_by('id')
    data = [
        ['N°','Code', 'Région', 'Nom de l\'agence'],
    ]
    
    counter = 1
    for agency in agencies:
        data.append([f"{counter}", f"{agency.code}", f"{agency.region}", f"{agency.name}"])
        counter +=1

    design_width = (0.4*inch, 1.2*inch, 1.2*inch, 2.5*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")


@login_required(login_url="/login/")
def exportpdf_profiles_view(request):
    name = "Profils"
    profiles = Profile.objects.all().order_by('uuid')
    data = [
        ['N°','Nom', 'Type', 'Statut', 'Contact', 'Adresse'],
    ]
    
    counter = 1
    for profile in profiles:
        data.append([f"{counter}", f"{profile.name}", f"{profile.type}", f"{profile.get_status_display()}", f"{profile.contact}", f"{profile.adresse}"])
        counter +=1

    design_width = (0.4*inch, 2.5*inch, 1.2*inch, 0.8*inch, 1.2*inch, 1.2*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")


@login_required(login_url="/login/")
def exportpdf_users_view(request):
    name = "Utilisateurs"
    users = CustomUser.objects.all().order_by('id')
    data = [
        ['N°','Prénom(s) & Nom', 'Type de profil', 'Email', 'Téléphone', 'Actif'],
    ]
    
    counter = 1
    for user in users:
        data.append([f"{counter}", f"{user.first_name} {user.last_name}", f"{user.profile.type}", f"{user.email}", f"{user.phone}", f"{user.is_active}"])
        counter +=1

    design_width = (0.4*inch, 2.5*inch, 1.2*inch, 2.0*inch, 1.0*inch, 0.5*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")


@login_required(login_url="/login/")
def exportpdf_permissions_view(request):
    name = "Permissions"
    permissions = Permission.objects.all().order_by('id')
    data = [
        ['N°','Nom', 'Type de profil', 'Autorisations'],
    ]
    
    counter = 1
    for permission in permissions:
        data.append([f"{counter}", f"{permission.name}", f"{permission.profile_type}", f"{permission.list}"])
        counter +=1

    design_width = (0.4*inch, 1.2*inch, 1.2*inch, 4.5*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")


@login_required(login_url="/login/")
def exportpdf_devises_view(request):
    name = "Dévises"
    devises = Devise.objects.all().order_by('id')
    data = [
        ['N°','Nom', 'Symbole', 'Valeur', 'Commentaires'],
    ]
    
    counter = 1
    for devise in devises:
        data.append([f"{counter}", f"{devise.name}", f"{devise.sign}", f"{devise.value}", f"{devise.comment}"])
        counter +=1

    design_width = (0.4*inch, 1.2*inch, 1.2*inch, 1.5*inch, 2.5*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")


@login_required(login_url="/login/")
def exportpdf_payments_view(request):
    name = "Paiements"
    payments = Payment.objects.all().order_by('id')
    data = [
        ['N°', 'Référence', 'Banque', 'Entreprise', 'Payeur', 'Montant', 'Date'],
    ]
    
    counter = 1
    for payment in payments:
        pay_date = DateFormat(payment.created_on)
        data.append([f"{counter}", f"N° 00{payment.id}/{pay_date.format('Y')}", f"{payment.created_by.profile.name}", f"{payment.facture_ref.client.name}", f"{payment.payer}", f"{to_amount(payment.amount)} {payment.devise.sign}", f"{pay_date.format('d/m/Y H:m')}"])
        counter +=1

    design_width = (0.4*inch, 0.9*inch, 1.2*inch, 1.2*inch, 1.5*inch, 1.6*inch, 1.2*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")

@login_required(login_url="/login/")
def exportpdf_bills_view(request):
    name = "Factures"
    bills = Facture.objects.all().order_by('id')
    data = [
        ['N°', 'Référence', 'Titre déclaration', 'Entreprise', 'Montant', 'Statut', 'Date'],
    ]
    
    counter = 1
    for bill in bills:
        pay_date = DateFormat(bill.created_on)
        data.append([f"{counter}", f"N° 00{bill.id}/{pay_date.format('Y')}", f"{bill.declaration_ref.title}", f"{bill.client.name}", f"{to_amount(bill.amount)} {bill.devise.sign}", f"{bill.get_status_display()}",  f"{pay_date.format('d/m/Y H:m')}"])
        counter +=1

    design_width = (0.4*inch, 0.9*inch, 1.5*inch, 1.2*inch, 1.9*inch, 0.7*inch, 1.2*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")


@login_required(login_url="/login/")
def exportpdf_declarations_view(request):
    name = "Déclarations"
    declarations = Declaration.objects.all().order_by('id')
    data = [
        ['N°', 'Référence', 'Entreprise', 'Titre', 'Total employés', 'Statut', 'Date'],
    ]
    
    counter = 1
    for declaration in declarations:
        pay_date = DateFormat(declaration.created_on)
        data.append([f"{counter}", f"N° 00{declaration.id}/{pay_date.format('Y')}", f"{declaration.created_by.profile.name}", f"{declaration.title}", f"{declaration.employees.count()}", f"{declaration.get_status_display()}",  f"{pay_date.format('d/m/Y H:m')}"])
        counter +=1

    design_width = (0.4*inch, 0.9*inch, 1.7*inch, 1.4*inch, 1.1*inch, 1.0*inch, 1.2*inch)
    
    file = export_pdf(name, data, design_width)

    return FileResponse(file, filename=f"export_pdf_{name}.pdf")


def export_xlsx(name, options, counter, col):
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()

    caption = f"LISTE DES {name.upper()}"
    page_header = 'apps/static/assets/img/bill/header_aguipee_tdss.png'
    number_format = workbook.add_format({"num_format": "$#,##0"})

    bold = workbook.add_format({"bold": True})
    worksheet.write_rich_string("C8",  bold, f"{caption}", " ")
    # worksheet.write("C8", caption)

    # worksheet.set_column("B:L", 20)
    worksheet.insert_image("A1", page_header, {"x_scale": 0.5, "y_scale": 0.5})

    worksheet.set_footer(f"&C{caption} &R&P")
    
    worksheet.add_table(f"B10:{col}{counter+9}", options)

    worksheet.autofit()

    workbook.close()
    buffer.seek(0)

    return buffer


@login_required(login_url="/login/")
def exportxlsx_agencies_view(request):

    name = "Agences"
    agencies = Agency.objects.all().order_by('id')
    data = []
    counter = 1
    for agency in agencies:
        data.append([f"{counter}", f"{agency.code}", f"{agency.region}", f"{agency.name}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Code'}, 
            {"header": 'Région'}, 
            {"header": 'Nom de l\'agence'},
        ]
    }

    file = export_xlsx(name, options, counter, 'E')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")


@login_required(login_url="/login/")
def exportxlsx_profiles_view(request):

    name = "Profils"
    profiles = Profile.objects.all().order_by('uuid')
    data = []
    counter = 1
    for profile in profiles:
        data.append([f"{counter}", f"{profile.name}", f"{profile.type}", f"{profile.get_status_display()}", f"{profile.contact}", f"{profile.adresse}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Nom'}, 
            {"header": 'Type'}, 
            {"header": 'Statut'},
            {"header": 'Contact'},
            {"header": 'Adresse'},
        ]
    }
    
    file = export_xlsx(name, options, counter, 'G')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")


@login_required(login_url="/login/")
def exportxlsx_users_view(request):

    name = "Utilisateurs"
    users = CustomUser.objects.all().order_by('id')
    data = []
    counter = 1
    for user in users:
        data.append([f"{counter}", f"{user.first_name} {user.last_name}", f"{user.profile.type}", f"{user.email}", f"{user.phone}", f"{user.is_active}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Prénom(s) & Nom'}, 
            {"header": 'Type de profil'}, 
            {"header": 'Email'},
            {"header": 'Téléphone'},
            {"header": 'Actif'},
        ]
    }
    
    file = export_xlsx(name, options, counter, 'G')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")


@login_required(login_url="/login/")
def exportxlsx_permissions_view(request):

    name = "Permissions"
    permissions = Permission.objects.all().order_by('id')
    data = []
    counter = 1
    for permission in permissions:
        data.append([f"{counter}", f"{permission.name}", f"{permission.profile_type}", f"{permission.list}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Nom'}, 
            {"header": 'Type de profil'}, 
            {"header": 'Autorisations'},
        ]
    }
    
    file = export_xlsx(name, options, counter, 'E')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")


@login_required(login_url="/login/")
def exportxlsx_devises_view(request):

    name = "Dévises"
    devises = Devise.objects.all().order_by('id')
    data = []
    counter = 1
    for devise in devises:
        data.append([f"{counter}", f"{devise.name}", f"{devise.sign}", f"{devise.value}", f"{devise.comment}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Nom'}, 
            {"header": 'Symbole'}, 
            {"header": 'Valeur'},
            {"header": 'Commentaires'},
        ]
    }
    
    file = export_xlsx(name, options, counter, 'F')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")


@login_required(login_url="/login/")
def exportxlsx_payments_view(request):

    name = "Paiements"
    payments = Payment.objects.all().order_by('id')
    data = []
    counter = 1
    for payment in payments:
        pay_date = DateFormat(payment.created_on)
        data.append([f"{counter}", f"N° 00{payment.id}/{pay_date.format('Y')}", f"{payment.created_by.profile.name}", f"{payment.facture_ref.client.name}", f"{payment.payer}", f"{payment.amount}", f"{payment.devise.sign}", f"{pay_date.format('d/m/Y H:m')}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Référence'}, 
            {"header": 'Banque'}, 
            {"header": 'Entreprise'},
            {"header": 'Payeur'},
            {"header": 'Montant'},
            {"header": 'Dévise'},
            {"header": 'Date'},
        ]
    }
    
    file = export_xlsx(name, options, counter, 'I')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")


@login_required(login_url="/login/")
def exportxlsx_bills_view(request):

    name = "Factures"
    bills = Facture.objects.all().order_by('id')
    data = []
    counter = 1
    for bill in bills:
        pay_date = DateFormat(bill.created_on)
        data.append([f"{counter}", f"N° 00{bill.id}/{pay_date.format('Y')}", f"{bill.declaration_ref.title}", f"{bill.client.name}", f"{bill.amount}", f"{bill.devise.sign}", f"{bill.get_status_display()}",  f"{pay_date.format('d/m/Y H:m')}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Référence'}, 
            {"header": 'Titre déclaration'}, 
            {"header": 'Entreprise'},
            {"header": 'Montant'},
            {"header": 'Dévise'},
            {"header": 'Statut'},
            {"header": 'Date'},
        ]
    }
    
    file = export_xlsx(name, options, counter, 'I')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")


@login_required(login_url="/login/")
def exportxlsx_declarations_view(request):

    name = "Déclarations"
    # declarations = Declaration.objects.all().order_by('id')
    if request.user.profile.type.code == ProfileType.ADMIN or request.user.type.code == UserType.TDSS:
        declarations = Declaration.objects.prefetch_related('employees').annotate(nb_employees=Count('declarationemployee')).all().order_by('created_on')
    elif request.user.type.code == UserType.AGUIPE:
        declarations = Declaration.objects.prefetch_related('employees').annotate(nb_employees=Count('declarationemployee')).filter(status='submitted').order_by('created_on')
    elif request.user.type.code == UserType.AGENT:
        declarations = Declaration.objects.prefetch_related('employees').annotate(nb_employees=Count('declarationemployee')).filter(created_by=request.user).order_by('created_on')
    else:
        declarations = Declaration.objects.prefetch_related('employees').annotate(nb_employees=Count('declarationemployee')).filter(created_by__profile=request.user.profile).order_by('created_on')
    
    data = []
    counter = 1
    for declaration in declarations:
        pay_date = DateFormat(declaration.created_on)
        data.append([f"{counter}", f"N° 00{declaration.id}/{pay_date.format('Y')}", f"{declaration.created_by.profile.name}", f"{declaration.title}", f"{declaration.employees.count()}", f"{declaration.get_status_display()}",  f"{pay_date.format('d/m/Y H:m')}"])
        counter +=1

    options = {
        "data": data, 
        # "style": "Table Style Light 11", 
        "columns": [
            {"header": 'N°'}, 
            {"header": 'Référence'}, 
            {"header": 'Entreprise'}, 
            {"header": 'Titre'},
            {"header": 'Total employés'},
            {"header": 'Statut'},
            {"header": 'Date'},
        ]
    }
    
    file = export_xlsx(name, options, counter, 'H')

    return FileResponse(file, as_attachment=True, filename=f"export_excel_{name.lower()}.xlsx")
