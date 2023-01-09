from django.contrib import admin

from .models import Devise, Facture, Payer, Payment

# Register your models here.

class DeviseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sign', 'value', 'comment')

class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'ref', 'date', 'amount', 'devise')

class PayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first', 'last', 'phone', 'employer', 'job')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ref', 'type', 'payer', 'date', 'amount', 'devise')

admin.site.register(Devise, DeviseAdmin)
admin.site.register(Facture, FactureAdmin)
admin.site.register(Payer, PayerAdmin)
admin.site.register(Payment, PaymentAdmin)