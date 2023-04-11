from django import template
from apps.paiement.models import JobCategory

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def count_employee_jobcategory(object, id_job_category):
    job_category = JobCategory.objects.get(pk=id_job_category)
    return object.filter(job_category=job_category).count()