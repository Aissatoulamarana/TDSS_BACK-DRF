from django import template
from apps.paiement.models import JobCategory
from apps.authentication.models import Profile, ProfileType, UserType, CustomUser

from django.utils.dateformat import DateFormat

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def count_employee_jobcategory(object, id_job_category):
    job_category = JobCategory.objects.get(pk=id_job_category)
    return object.filter(job_category=job_category).count()


@register.filter
def count_by_status(object, status):
    return object.filter(status=status).count()


@register.filter
def count_by_profile_type(object, uid_profile_type):
    profile_type = ProfileType.objects.get(uid=uid_profile_type)
    return object.filter(type=profile_type).count()


@register.filter
def count_by_user_type(object, uid_user_type):
    user_type = UserType.objects.get(uid=uid_user_type)
    return object.filter(type=user_type).count()


@register.filter
def count_by_profile(object, id_profile):
    profile = Profile.objects.get(pk=id_profile)
    return object.filter(type=profile).count()


@register.filter
def to_amount(number):
    return "{:0,.0f}".format(number).replace(','," ")


@register.filter
def get_reference(element):
    date = DateFormat(element.created_on)
    reference = f"N° 00{element.id}/{date.format('Y')}"

    return reference
