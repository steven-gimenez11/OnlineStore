from django import template

register = template.Library()

@register.filter(name='formato_precio')
def formato_precio(value):
    """Formatea un valor numérico como un precio con dos decimales en formato europeo."""
    try:
        return "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return value


@register.filter(name='mul')
def mul(value, arg):
    """Multiplica el valor (precio) por el argumento (cantidad)."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0
