# import viewsets
from rest_framework import viewsets, permissions
 
# import local data
from .serializers import DeclarationSerializer
from .models import Declaration
 
# create a viewset
class DeclarationViewSet(viewsets.ModelViewSet):

    # Check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # define queryset
    queryset = Declaration.objects.all()
     
    # specify serializer to be used
    serializer_class = DeclarationSerializer