from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplie deux valeurs."""
    return value * arg