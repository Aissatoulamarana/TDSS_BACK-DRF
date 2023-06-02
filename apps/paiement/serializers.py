# importing serializer from rest_framework
from rest_framework import serializers

# importing model from models.py
from .models import Payment, Employee, Payer, Declaration, Facture, JobCategory, Job
from apps.authentication.models import CustomUser, Profile, ProfileType


class ProfileSerializer(serializers.ModelSerializer):
    # type = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'name', 'type', 'location', 'contact', 'status', 'email', 'adresse', 'created_on')


class FactureSerializer(serializers.ModelSerializer):
    # client = ProfileSerializer(read_only=True)
    client = serializers.StringRelatedField(read_only=True)
    devise = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Facture
        fields = ('id', 'reference', 'client', 'amount', 'devise', 'created_on')


class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = ('first', 'last', 'phone', 'country_origin', 'address')


class PaymentSerializer(serializers.ModelSerializer):
    facture_ref = FactureSerializer(read_only=True)
    payer = PayerSerializer(read_only=True)
    devise = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Payment
        fields = ('id', 'reference', 'facture_ref', 'payer', 'amount', 'devise', 'created_on')


# Create declaration model serializer
class DeclarationSerializer(serializers.ModelSerializer):
    # specify model and fields
    class Meta:
        model = Declaration
        fields = ('id', 'reference', 'title', 'status', 'comment', 'created_on')


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ('id', 'name', 'permit')


class EmployeeSerializer(serializers.ModelSerializer):
    declaration = DeclarationSerializer(read_only=True)
    job_category = JobCategorySerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'declaration', 'job_category', 'job', 'passport_number', 'first', 'last', 'email', 'phone']