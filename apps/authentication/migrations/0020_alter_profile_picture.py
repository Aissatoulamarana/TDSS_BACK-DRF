# Generated by Django 4.0.8 on 2023-05-26 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_alter_permission_codes_alter_permission_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures', verbose_name='profile picture'),
        ),
    ]
