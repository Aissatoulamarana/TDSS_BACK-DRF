# Generated by Django 4.0.8 on 2023-05-05 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_permission_permissions_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='permissions_code',
            new_name='codes',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='permissions_list',
            new_name='list',
        ),
        migrations.AddField(
            model_name='customuser',
            name='permissions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customuser_permissions', to='authentication.permission'),
        ),
        migrations.AddField(
            model_name='permission',
            name='profile_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='permissions_profile_types', to='authentication.profiletype'),
            preserve_default=False,
        ),
    ]
