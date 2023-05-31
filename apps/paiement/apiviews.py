# import viewsets
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
 
# import local data
from .serializers import DeclarationSerializer, EmployeeSerializer
from .models import Declaration, Employee

 
# Declaration viewsets
class DeclarationViewSet(viewsets.ModelViewSet):

    # Check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # define queryset
    queryset = Declaration.objects.all()
     
    # specify serializer to be used
    serializer_class = DeclarationSerializer


@api_view(['GET', 'POST'])
def employee_list(request, format=None):
    """
    List all employees, or create a new employee.
    """
    
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pid, format=None):
    """
    Retrieve, update or delete an employee.
    """
    try:
        employee = Employee.objects.get(passport_number=pid)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
