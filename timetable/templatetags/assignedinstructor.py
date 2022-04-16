from django import template

register = template.Library()


@register.filter('assignedinstructor')
def assignedinstructor(instructors, section):
    return instructors.filter(section=section).first()