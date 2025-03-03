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
        fields = '__all__'

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
        read_only_fields = ('created_on', 'created_by') 

# # Create declaration model serializer
# class DeclarationSerializer(serializers.ModelSerializer):
#     # specify model and fields
#     class Meta:
#         model = Declaration
#         fields = ('id', 'reference', 'title', 'status', 'comment', 'created_on')


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ('id', 'name', 'permit')


class JobSerializer(serializers.ModelSerializer):
    number_person = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ["id", "name", "category", "created_at", "number_person"]

    def get_number_person(self, obj):
        return obj.get_person_count()
    def validate_name(self, value):
        if Job.objects.filter(name=value).exists():
            raise serializers.ValidationError("Une fonction avec ce nom existe déjà.")
        return value


class EmployeeSerializer(serializers.ModelSerializer):
    # job_detail = JobSerializer(read_only=True)
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    job_category = JobCategorySerializer(read_only=True)
    class Meta:
        model = Employee
        fields = ('id',  'job', 'job_category', 'passport_number', 'first', 'last', 'email', 'phone')

class DeclarationSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)
    total_amount = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()  # Nouveau champ

    class Meta:
        model = Declaration
        fields = (
           'id', 'reference', 'title', 'status', 'reject_reason', 'comment',
            'created_by', 'employees', 'total_amount', 'employee_count', 'created_on'
        )
        read_only_fields = ('reference', 'status', 'total_amount', 'employee_count', 'created_by')

    def get_total_amount(self, obj):
        total = 0
        for employee in obj.employee_declarations.all():
            print(f"Employee: {employee}, Job: {employee.job}, Category: {employee.job_category if employee.job else 'None'}")
            if employee.job and employee.job.category and employee.job.category.permit:
                print(f"Permit Price: {employee.job.category.permit.price}, Permis: {employee.job.category.permit}")
                total += employee.job.category.permit.price
        print(f"Total Amount: {total}")
        return total


    def get_employee_count(self, obj):
        # On retourne simplement le nombre d'employés liés à la déclaration.
        # Ici on suppose que "employee_declarations" est le related_name de la FK "declaration" dans Employee
        return obj.employee_declarations.count()

    def create(self, validated_data):
        employees_data = validated_data.pop('employees', [])
        # Forcer le status à "submitted"
        validated_data['status'] = Declaration.SUBMITTED

        # Récupérer l'utilisateur connecté depuis le contexte
        validated_data['created_by'] = self.context['request'].user

        declaration = Declaration.objects.create(**validated_data)
        for employee_data in employees_data:
            # Créer l'employée en liant la déclaration via la FK "declaration"
            Employee.objects.create(declaration=declaration, **employee_data)
        return declaration
    

# serializers.py
class EmployeeDetailSerializer(serializers.ModelSerializer):
    fonction = serializers.SerializerMethodField()
    permis = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "passport_number",
            "first",
            "last",
            "phone",
            "fonction",
            "permis",
            "category",
        )

    def get_fonction(self, obj):
        # Si le champ "job" est renseigné, retourne son nom, sinon None
        return obj.job.name if obj.job else None
    
    def get_category(self, obj):
        #On récupère la category via le job 
        if obj.job and obj.job_category:
            return obj.job_category.name
        return None
    
    def get_permis(self, obj):
        # On récupère le permis via le job, sa catégorie et le permis associé
        if obj.job and obj.job_category and obj.job_category.permit:
            return obj.job_category.permit.name  # ou toute autre info pertinente
        return None

class DeclarationDetailSerializer(serializers.ModelSerializer):
    # On utilise ici le serializer dédié aux détails des employés
    employees = EmployeeDetailSerializer(source="employee_declarations", many=True, read_only=True)

    class Meta:
        model = Declaration
        fields = (
            "reference",
            "title",
            "status",
            "reject_reason",
            "comment",
            "created_by",
            "created_on",
            "employees",
        )


class DeclarationEditSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)
    total_amount = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()

    class Meta:
        model = Declaration
        fields = (
            'id', 'reference', 'title',  'comment','modified_by', 
            'created_by', 'employees', 'total_amount', 'employee_count', 'created_on'
        )
        read_only_fields = ('reference', 'status', 'total_amount', 'employee_count', 'created_by')


    def get_total_amount(self, obj):
        total = 0
        for employee in obj.employee_declarations.all():
            if employee.job and employee.job.category and employee.job.category.permit:
                total += employee.job.category.permit.price
        return total

    def get_modified_by(self, obj):
        """ Récupère l'utilisateur ayant effectué la modification (depuis la requête) """
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user.username  # Retourne le username de l'utilisateur
        return None  # Si pas d'utilisateur connecté
    def update(self, instance, validated_data):
        employees_data = validated_data.pop('employees', [])
        
        # Mise à jour des autres champs de la déclaration
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Obtenir les employés existants
        existing_employee_ids = set(instance.employees.values_list('id', flat=True))
        received_employee_ids = {emp.get('id') for emp in employees_data if 'id' in emp}

        #  Supprimer les employés qui ne sont plus dans la déclaration
        employees_to_delete = existing_employee_ids - received_employee_ids
        Employee.objects.filter(id__in=employees_to_delete).delete()

        #  Modifier les employés existants
        for emp_data in employees_data:
            emp_id = emp_data.get('id', None)
            if emp_id in existing_employee_ids:
                employee = Employee.objects.get(id=emp_id)
                for key, value in emp_data.items():
                    setattr(employee, key, value)
                employee.save()

        #  Ajouter de nouveaux employés
        for emp_data in employees_data:
            if 'id' not in emp_data:  # S'il n'y a pas d'ID, c'est un nouvel employé
                Employee.objects.create(declaration=instance, **emp_data)

        return instance
