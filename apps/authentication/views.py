# # -*- encoding: utf-8 -*-
# """
# Copyright (c) 2022 - OD
# """

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from apps.authentication.serializers import AgencySerializer, PermissionSerializer, ProfileSerializer
from .forms import LoginForm, SignUpForm, ProfileForm, CustomUserForm, ResetPwdForm, AgencyForm, PermissionForm
from .models import CustomUser, ProfileType, Profile, Region, Agency, UserType, Menu, SubMenu, Action, Permission
from apps.paiement.models import Devise
import secrets, string
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib import messages
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Create your views here.


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist le token

            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# # Global devises for all views
# devises = Devise.objects.all().order_by('id')

# def users_view(request):
#     if request.user.profile.type.uid == 1:
#         users = CustomUser.objects.all().order_by('-modified_on')
#     elif request.user.type.uid == 2:
#         users = CustomUser.objects.filter(created_by=request.user).order_by('-created_on')
#     else:
#         users = CustomUser.objects.filter(created_by__profile=request.user.profile)

#     return render(request, "accounts/users.html", {
#         'users': users,
#         'taux': devises,
#         'segment': "administration"
#     })


class DeactivateUserView(APIView):
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.is_active = False
            user.save()
            return Response({"message": "Compte utilisateur désactivé."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)


class ProfileListView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def add_profile_api(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        profileform = ProfileForm(request.data, request.FILES, prefix="profile")
        userform = CustomUserForm(request.data, prefix="user")

        # Make 'type' field optional in user form
        userform.fields["type"].required = False
        
        if profileform.is_valid() and userform.is_valid():
            # Save the profile
            new_profile = profileform.save(commit=False)
            new_profile.save()
            
            # Create a random password for the user
            random_pwd = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8))

            # Save the user
            new_user = userform.save(commit=False)
            new_user.username = new_user.email
            new_user.set_password(random_pwd)
            new_user.created_by = request.user  # assuming request.user is the current logged-in user
            new_user.type = UserType.objects.first()  # make sure UserType is defined
            new_user.profile = new_profile
            new_user.save()

            # Send confirmation email
            send_mail(
                "Creation de nouveau compte",
                f"Bonjour {new_user.first_name} {new_user.last_name}, \n\nUn compte a été créé pour vous sur le portail de télédéclaration des employés non-nationaux. \nCi-dessous vos informations d'accès. \n\nEmail: {new_user.email}\nMot de Passe: {random_pwd}\n\nAller sur: https://workpermit.tdss.com.gn pour vous connecter. \nCordialement",
                "noreply@tdss.com.gn",
                [new_user.email],
                fail_silently=True
            )

            # Return success response
            return Response({"message": "Nouveau profil ajouté. Un compte utilisateur a été créé pour le responsable."}, status=status.HTTP_201_CREATED)
        
        # If forms are invalid, return error response with the form errors
        errors = {}
        if not profileform.is_valid():
            errors['profileform'] = profileform.errors
        if not userform.is_valid():
            errors['userform'] = userform.errors
        
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(pk=profile_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"error": "Profil introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, profile_id):
        try:
            profile = Profile.objects.get(pk=profile_id)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error": "Profil introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, profile_id):
        try:
            profile = Profile.objects.get(pk=profile_id)
            profile.delete()
            return Response({"message": "Profil supprimé"}, status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return Response({"error": "Profil introuvable"}, status=status.HTTP_404_NOT_FOUND)

class AgencyListView(APIView):
    def get(self, request):
        agencies = Agency.objects.all()
        serializer = AgencySerializer(agencies, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def add_agency_view(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    # Serializer de l'agence
    if request.method == 'POST':
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Nouvelle agence ajoutée."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyDetailView(APIView):
    def get(self, request, agency_id):
        try:
            agency = Agency.objects.get(pk=agency_id)
            serializer = AgencySerializer(agency)
            return Response(serializer.data)
        except Agency.DoesNotExist:
            return Response({"error": "Agence introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, agency_id):
        try:
            agency = Agency.objects.get(pk=agency_id)
            serializer = AgencySerializer(agency, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Agency.DoesNotExist:
            return Response({"error": "Agence introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, agency_id):
        try:
            agency = Agency.objects.get(pk=agency_id)
            agency.delete()
            return Response({"message": "Agence supprimée"}, status=status.HTTP_204_NO_CONTENT)
        except Agency.DoesNotExist:
            return Response({"error": "Agence introuvable"}, status=status.HTTP_404_NOT_FOUND)


class PermissionListView(APIView):
    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def add_permission_view(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    # Serializer de la permission
    if request.method == 'POST':
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Nouvelle permission ajoutée."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PermissionDetailView(APIView):
    def get(self, request, permission_id):
        try:
            permission = Permission.objects.get(pk=permission_id)
            serializer = PermissionSerializer(permission)
            return Response(serializer.data)
        except Permission.DoesNotExist:
            return Response({"error": "Permission introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, permission_id):
        try:
            permission = Permission.objects.get(pk=permission_id)
            serializer = PermissionSerializer(permission, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Permission.DoesNotExist:
            return Response({"error": "Permission introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, permission_id):
        try:
            permission = Permission.objects.get(pk=permission_id)
            permission.delete()
            return Response({"message": "Permission supprimée"}, status=status.HTTP_204_NO_CONTENT)
        except Permission.DoesNotExist:
            return Response({"error": "Permission introuvable"}, status=status.HTTP_404_NOT_FOUND)
