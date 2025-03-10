# Generated by Django 4.0.8 on 2023-01-09 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0012_profile_adresse_profile_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('sign', models.CharField(max_length=3)),
                ('value', models.DecimalField(decimal_places=2, default=1, max_digits=7)),
                ('comment', models.TextField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('comment', models.TextField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('devise', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='facture_devises', to='paiement.devise')),
            ],
        ),
        migrations.CreateModel(
            name='Payer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=100, verbose_name='first name')),
                ('last', models.CharField(max_length=50, verbose_name='last_name')),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.IntegerField()),
                ('country_origin', models.CharField(blank=True, max_length=100, null=True)),
                ('job', models.CharField(blank=True, max_length=50, null=True)),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authentication.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('comment', models.TextField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('devise', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_devises', to='paiement.devise')),
                ('facture_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='paiement.facture')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_payers', to='paiement.payer')),
            ],
        ),
    ]
