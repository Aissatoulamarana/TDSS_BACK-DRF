# Generated by Django 4.2 on 2024-10-17 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paiement', '0020_employee_created_on_employee_modified_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
