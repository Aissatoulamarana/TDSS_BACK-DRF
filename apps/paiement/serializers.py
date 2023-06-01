# importing serializer from rest_framework
from rest_framework import serializers

# importing model from models.py
from .models import Payment, Employee, Payer, Declaration, Facture

# Create declaration model serializer
class DeclarationSerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = Declaration
        fields = ('id', 'reference', 'title', 'status', 'comment', 'created_on')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'declaration', 'job_category', 'job', 'passport_number', 'first', 'last', 'email', 'phone']