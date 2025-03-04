from django.contrib import admin

from .models import (Devise, Facture, Payer, Payment,
                     Permit, JobCategory, Job, Country, Declaration, Employee,
                     DeclarationEmployee)

# Register your models here.


class DeviseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sign', 'value', 'comment')

class DeclarationEmployeInline(admin.TabularInline):
    # list_display = ('employee', 'declaration', 'created_on')
    fields = ('employee', 'declaration', )
    model = DeclarationEmployee


class DeclarationAdmin(admin.ModelAdmin):
    search_fields = ('title', 'reference',)
    list_filter = ('status', )
    list_display = ('id', 'reference', 'title', 'status', 'comment', 'created_by')
    list_display_links = ('id', 'reference', 'title')
    inlines = [DeclarationEmployeInline,]
    extra = 2



class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('passport_number', 'phone', 'first', 'last')
    list_display = ('id', 'declaration', 'passport_number', 'first', 'last', 'phone', 'job_category', 'job')
    inlines = [DeclarationEmployeInline,]


class DeclarationEmployeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'declaration', 'created_on')
    fields = ('employee', 'declaration', )


class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'client', 'amount', 'devise')


class PayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first', 'last', 'phone', 'employer', 'job')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'type', 'payer', 'amount', 'devise')


class PermitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price', 'devise', 'comment')


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'permit', 'status', 'comment')


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'status', 'comment')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'comment')


admin.site.register(Devise, DeviseAdmin)
admin.site.register(Declaration, DeclarationAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DeclarationEmployee, DeclarationEmployeAdmin)
admin.site.register(Facture, FactureAdmin)
admin.site.register(Payer, PayerAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Permit, PermitAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Country, CountryAdmin)
