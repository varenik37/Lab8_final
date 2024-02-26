from django import template
from test_django.models import Employee

register = template.Library()

@register.simple_tag()
def all_name_student():
    return ", ".join([(employee.first_name + employee.last_name) for employee in Employee.objects.all()])



