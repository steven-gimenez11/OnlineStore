from django import template

register = template.Library()

@register.filter(name='formato_precio')
def formato_precio(value):
    """Format value as currency (e.g., $100.00)."""
    try:
        return "${:,.2f}".format(value)
    except (ValueError, TypeError):
        return value


@register.filter(name='mul')
def mul(value, arg):
    """Multiplica el valor (precio) por el argumento (cantidad)."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0
