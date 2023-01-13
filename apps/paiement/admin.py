from django.contrib import admin

from .models import Devise, Facture, Payer, Payment, Permit, Job, Country

# Register your models here.

class DeviseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sign', 'value', 'comment')

class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'amount', 'devise')

class PayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first', 'last', 'phone', 'employer', 'job')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'type', 'payer', 'amount', 'devise')

class PermitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price', 'devise', 'comment')

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'comment')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'comment')

admin.site.register(Devise, DeviseAdmin)
admin.site.register(Facture, FactureAdmin)
admin.site.register(Payer, PayerAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Permit, PermitAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Country, CountryAdmin)