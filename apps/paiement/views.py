# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

from uuid import UUID
import copy

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status
from .serializers import DeclarationDetailSerializer, DeclarationEditSerializer, DeclarationSerializer, FactureSerializer, JobCategorySerializer, JobSerializer, PayerSerializer, PaymentSerializer
from .permissions import IsAdminOrCanViewAll, IsClientOrAgent
from apps.paiement.models import (
    Devise,
    Facture,
    Payer,
    Payment,
    Permit,
    Employee,
    Declaration,
    DeclarationEmployee,
    JobCategory,
    Job,
)
from apps.authentication.models import Profile, CustomUser, ProfileType, UserType
from .forms import (
    DeviseForm,
    FactureForm,
    PayerForm,
    PaymentForm,
    EmployeeForm,
    EmployeeRenewForm,
    DeclarationForm,
)

# Global devises for all views
devises = Devise.objects.all().order_by("id")

@api_view(['GET'])
def job_category_list(request):
    job_categories = JobCategory.objects.all()
    serializer = JobCategorySerializer(job_categories, many=True)
    return Response(serializer.data)

# api pour ajouter et recuperer la liste des fonctions
@api_view(["GET", "POST"])
def job_list(request):
    """
    - `GET` : Récupère toutes les fonctions avec le nombre de personnes.
    - `POST` : Ajoute une nouvelle fonction.
    """
    if request.method == "GET":
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT", "PATCH", "DELETE"])
def job_update(request, job_id):
    """
    - `PUT` : Met à jour entièrement un job.
    - `PATCH` : Met à jour partiellement un job.
    - `DELETE` : Supprime un job.
    """
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'error': 'Job non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ["PUT", "PATCH"]:
        serializer = JobSerializer(job, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        job.delete()
        return Response({"message": "Job supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
@api_view([ 'POST'])
def declaration_create(request):
    if request.method == 'POST':
        serializer = DeclarationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#api pour voir la liste des declarations 
@api_view(['GET'])
@permission_classes([ IsAdminOrCanViewAll])
def declaration_list(request):
    # Check user role
    if request.user.is_superuser or request.user.profile.type.code == 'ADMIN' or request.user.type.code == 'TDSS':
        declarations = (
            Declaration.objects.prefetch_related("employees")
            .annotate(nb_employees=Count("declarationemployee"))
            .all()
            .order_by("created_on")
        )
    elif request.user.type.code == 'AGUIPE':
        declarations = (
            Declaration.objects.prefetch_related("employees")
            .annotate(nb_employees=Count("declarationemployee"))
            .filter(status="submitted")
            .order_by("created_on")
        )
    elif request.user.type.code == 'AGENT':
        declarations = (
            Declaration.objects.prefetch_related("employees")
            .annotate(nb_employees=Count("declarationemployee"))
            .filter(created_by=request.user)
            .order_by("created_on")
        )
    else:
        declarations = (
            Declaration.objects.prefetch_related("employees")
            .annotate(nb_employees=Count("declarationemployee"))
            .filter(created_by__profile=request.user.profile)
            .order_by("created_on")
        )
    
    # Serialize the querysets
    serializer = DeclarationSerializer(declarations, many=True)

    # Return serialized data as JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


#api pour modifier les informations d'une declaration 
@api_view(["PUT"])
def edit_declaration_api(request, declaration_id):
    try:
        #  Récupérer la déclaration existante
        declaration = get_object_or_404(Declaration, pk=declaration_id)

        #  Envoyer les données au serializer pour mise à jour
        serializer = DeclarationEditSerializer(declaration, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#api pour voir si le numero de passeport existe 
@api_view(['GET'])
def check_passport(request):
    """
    Vérifie si un numéro de passeport existe.
    Exemples d'URL :
      - /api/check-passport/?numero=A123456
    """
    passport = request.query_params.get('numero')
    if not passport:
        return Response(
            {"detail": "Le paramètre 'passport' est requis."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = Employee.objects.filter(passport_number=passport).exists()
    return Response({"exists": exists}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])  # Désactive temporairement l'authentification
def declaration_detail(request, pk):
    print("Utilisateur authentifié :", request.user)  # Voir si ça s'affiche maintenant
    try:
        declaration = Declaration.objects.get(pk=pk)
    except Declaration.DoesNotExist:
        return Response({"error": "Declaration not found."}, status=404)

    serializer = DeclarationDetailSerializer(declaration)
    return Response(serializer.data)

@api_view(['POST'])
def declaration_status_update(request, pk):
    """
    Vue pour valider ou rejeter une déclaration.
    """
    declaration = get_object_or_404(Declaration, pk=pk)
    action = request.data.get("action")

    if action == "validate":
        declaration.status = Declaration.VALIDATED
        declaration.reject_reason = ""  # Effacer le motif de rejet si présent
    elif action == "reject":
        reject_reason = request.data.get("reject_reason")
        if not reject_reason:
            return Response(
                {"error": "Le motif de rejet est requis pour rejeter une déclaration."},
                status=status.HTTP_400_BAD_REQUEST
            )
        declaration.status = Declaration.REJECTED
        declaration.reject_reason = reject_reason
    else:
        return Response(
            {"error": "Action invalide. Utilisez 'validate' ou 'reject'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    declaration.save()
    serializer = DeclarationDetailSerializer(declaration)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def facturer_declaration_api(request, declaration_id):
    # Récupérer la déclaration ou renvoyer une 404
    declaration = get_object_or_404(Declaration, pk=declaration_id)
    
    # Récupérer les catégories de métiers
    cadres = get_object_or_404(JobCategory, pk=1)
    agents = get_object_or_404(JobCategory, pk=2)
    ouvriers = get_object_or_404(JobCategory, pk=3)
    
    # Pour le test : si le profil du client est null, utiliser request.user.profile ou un profil de secours
    client_profile = getattr(declaration.created_by, 'profile', None)
    if client_profile is None:
        client_profile = getattr(request.user, 'profile', None)
        if client_profile is None:
            # Optionnel : récupère le premier profil disponible dans la base (à ne pas utiliser en prod)
            client_profile = Profile.objects.first()
    
    # Création d'une instance de facture
    facture = Facture(
        declaration_ref=declaration,
        client=client_profile,
        total_cadres=declaration.employees.filter(job_category=cadres).count(),
        total_agents=declaration.employees.filter(job_category=agents).count(),
        total_ouvriers=declaration.employees.filter(job_category=ouvriers).count(),
        amount=0,  # Valeur temporaire
        devise=cadres.permit.devise,
        created_by=request.user
    )
    
    # Calcul du montant total
    facture.amount = (
        (facture.total_cadres * cadres.permit.price) +
        (facture.total_agents * agents.permit.price) +
        (facture.total_ouvriers * ouvriers.permit.price)
    )
    
    facture.save()
    
    declaration.status = "Facturée"
    declaration.save()
    
    serializer = FactureSerializer(facture)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([ IsAdminOrCanViewAll])
def factures_view_api(request):
    if (
        request.user.is_superuser  # Vérification si l'utilisateur est un super utilisateur
        or request.user.profile.type.code == 'ADMIN'
        or request.user.type.code == 'TDSS'
    ):
        factures = Facture.objects.select_related("client", "declaration_ref").all().order_by("created_on")
    elif request.user.type.code == 'AGENT':
        factures = Facture.objects.select_related("client", "declaration_ref").filter(status="unpaid").order_by("created_on")
    else:
        factures = Facture.objects.select_related("client", "declaration_ref").filter(created_by__profile=request.user.profile).order_by("created_on")
    
    serializer = FactureSerializer(factures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def facture_detail(request, pk):
    try:
        facture = Facture.objects.get(pk=pk)
    except Facture.DoesNotExist:
        return Response({"error": "Facture not found."}, status=404)

    serializer = FactureSerializer(facture)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([ IsAdminOrCanViewAll])
def list_paiements(self, request):
        """Récupère la liste des paiements en fonction du rôle de l'utilisateur."""
        user = request.user

        # Filtrage des paiements selon le rôle
        if (
        request.user.is_superuser  # Vérification si l'utilisateur est un super utilisateur
        or request.user.profile.type.code == 'ADMIN'
        or request.user.type.code == 'TDSS'
    ):
            payments = Payment.objects.all().order_by("created_on")
        elif user.type.code == UserType.AGENT:
            payments = Payment.objects.filter(created_by=user).order_by("created_on")
        else:
            payments = Payment.objects.filter(created_by__profile=user.profile).order_by("created_on")

        # Sérialiser les données et les retourner
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def paid_facture(request, facture_id):
    """
    API pour marquer une facture comme payée.
    """
    try:
        # Récupérer la facture à partir de l'ID
        facture = get_object_or_404(Facture, id=facture_id)

        # Vérifier que la facture n'est pas déjà payée
        if facture.status == "paid":
            return Response({
                "error": "Cette facture a déjà été payée."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Formulaire de paiement et de payeur
        payment_data = request.data.get('payment', {})
        payer_data = request.data.get('payer', {})

        # Sérialisation des données
        payer_serializer = PayerSerializer(data=payer_data)
        payment_serializer = PaymentSerializer(data=payment_data)

        if payer_serializer.is_valid() and payment_serializer.is_valid():
            # Sauvegarder les données payeur et paiement
            new_payer = payer_serializer.save(employer=facture.client)
            new_payment = payment_serializer.save(
                facture_ref=facture, 
                payer=new_payer,
                created_by=request.user
            )

            # Mise à jour du statut de la facture
            facture.status = "paid"
            facture.save()

            return Response({
                "message": "Paiement généré avec succès.",
                "payment": payment_serializer.data,
                "payer": payer_serializer.data,
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": "Les formulaires sont invalides.",
            "payment_errors": payment_serializer.errors,
            "payer_errors": payer_serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    except Facture.DoesNotExist:
        return Response({
            "error": "Facture non trouvée."
        }, status=status.HTTP_404_NOT_FOUND)

@login_required(login_url="/login/")
def add_payment_view(request):
    default_devise = Devise.objects.first()
    initial_value = {"devise": default_devise}
    context_empty = {
        "paymentform": PaymentForm(prefix="payment", initial=initial_value),
        "payerform": PayerForm(prefix="payer"),
        "taux": devises,
        "segment": "paiements",
    }

    if request.method == "POST":

        paymentform = PaymentForm(request.POST, prefix="payment")
        payerform = PayerForm(request.POST, prefix="payer")

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
                "paymentform": paymentform,
                "payerform": payerform,
                "ErrorMessage": "Formulaire invalid soumit",
                "taux": devises,
                "segment": "paiements",
            }
            return render(request, "paiements/add-payment.html", context)
    return render(request, "paiements/add-payment.html", context_empty)




@login_required(login_url="/login/")
def devises_view(request):
    devises = Devise.objects.all().order_by("id")
    guinean_franc = Devise.objects.first()
    dollar = Devise.objects.get(pk=2)
    euro = Devise.objects.get(pk=3)

    return render(
        request,
        "paiements/devises.html",
        {
            "guinean_franc": guinean_franc,
            "dollar": dollar,
            "euro": euro,
            "devises": devises,
            "taux": devises,
            "segment": "paiements",
        },
    )


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
        return render(
            request,
            "paiements/devises.html",
            {
                "guinean_franc": Devise.objects.first(),
                "dollar": Devise.objects.get(pk=2),
                "euro": Devise.objects.get(pk=3),
                "devises": devises,
                "taux": devises,
                "segment": "paiements",
            },
        )
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
            return JsonResponse({"error": "Type de permis inexistant."})

        try:
            devise = Devise.objects.get(pk=devise_id)
        except Devise.DoesNotExist:
            return JsonResponse({"error": "Devise inexistante."})

        return JsonResponse(
            {"permit_price": permit.price, "devise_value": devise.value}
        )
    else:
        return JsonResponse({"error": "Erreur requête. Contactez l'admin."})


def get_devise(request, devise_id):
    if request.method == "GET":

        try:
            devise = Devise.objects.get(pk=devise_id)
        except Devise.DoesNotExist:
            return JsonResponse({"error": "Devise inexistante."})

        return JsonResponse({"devise_value": devise.value})
    else:
        return JsonResponse({"error": "Erreur requête. Contactez l'admin."})




@login_required(login_url="/login/")
def declaration_employee_renew(request, declaration_id):
    form = EmployeeRenewForm(request.POST)
    if form.is_valid():
        validated_data = form.cleaned_data
        try:
            employee = Employee.objects.get(
                passport_number=validated_data["passport_number"]
            )
            declaration = Declaration.objects.get(pk=declaration_id)
            # print(validated_data['passport_number'], employee.passport_number)
            if employee.declaration == declaration:
                messages.error(request, "Il  a déjà été ajouté à cette déclaration")
                return redirect("paiement:edit_declaration", declaration_id)
            # ajouter l'employé a cette nouvelle declaration
            employee.declaration = declaration
            with transaction.atomic():
                employee.save()
                DeclarationEmployee.objects.create(
                    employee=employee, declaration=declaration
                )
            messages.success(
                request=request, message="L'employé a été ajouté avec succès"
            )
        except Employee.DoesNotExist as e:
            messages.error(request, "Pas de correspondance trouvé")
        except Declaration.DoesNotExist as e:
            messages.error(request, "Cette déclaration n'existe pas")
    else:
        messages.error(request, "Vous devez saisir un numéro valide de passport")
    return redirect("paiement:edit_declaration", declaration_id)






@login_required(login_url="/login/")
def add_facture_view(request):
    default_devise = Devise.objects.first()
    initial_value = {"devise": default_devise}
    context_empty = {
        "factureform": FactureForm(initial=initial_value),
        "permits": Permit.objects.all(),
        "taux": devises,
        "segment": "facturation",
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
                "factureform": factureform,
                "ErrorMessage": "Formulaire invalid soumit",
                "taux": devises,
                "segment": "facturation",
            }
            return render(request, "paiements/add-facture.html", context)

    return render(request, "paiements/add-facture.html", context_empty)
