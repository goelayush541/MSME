from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.simple_tag
def is_enrolled(user, course):
    return Enrollment.objects.filter(user=user, course=course).exists()