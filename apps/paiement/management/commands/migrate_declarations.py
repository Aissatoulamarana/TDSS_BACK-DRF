from django.core.management.base import BaseCommand, CommandError
from apps.paiement.models import Declaration, DeclarationEmployee, Employee


class Command(BaseCommand):
    help = "Cette commande permet de migrer les anciennes declarations"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        nb_migrated_declarations = 0
        try:
            declarations = Declaration.objects.prefetch_related('employee_declarations').prefetch_related('employees').all()
            NB_ALL = declarations.count()
            # for declaration in declarations:
            #     print(declaration.employee_declarations.count(), end=' ')
            #     print(declaration.employees.count())
            for index, declaration in enumerate(declarations):
                self.stdout.write(
                self.style.HTTP_INFO(f'====== {index + 1}/{NB_ALL} ========')
                )
                if declaration.employees.count() != 0:
                    continue
                for employee in declaration.employee_declarations.all():
                    DeclarationEmployee.objects.create(declaration=declaration, employee=employee)
                nb_migrated_declarations += 1 
                
        except Exception as e:
            raise e
        else:
            pass
        finally:
            self.stdout.write(
                self.style.SUCCESS(f' {nb_migrated_declarations} déclarations ont été migrées avec succès')
            )
        

        

            
