# Generated by Django 4.1.6 on 2023-06-03 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0021_remove_profile_account_remove_profile_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiletype',
            name='comment',
        ),
    ]
