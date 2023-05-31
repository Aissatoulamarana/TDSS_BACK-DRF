# importing serializer from rest_framework
from rest_framework import serializers

# importing model from models.py
from .models import Payment, Employee, Payer, Declaration, Facture

# Create a model serializer
class DeclarationSerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = Declaration
        fields = ('title', 'comment')