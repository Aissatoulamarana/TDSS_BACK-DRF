# Generated by Django 4.0.8 on 2022-12-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_customuser_job_customuser_phone_profile_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='reset_pwd',
            field=models.BooleanField(default=True),
        ),
    ]
