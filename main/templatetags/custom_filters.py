# main/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def abs_val(value):
    """Return absolute value of a number"""
    return abs(value)