from django import template

register = template.Library()

@register.filter(name='formato_precio')
def formato_precio(value):

    return "${:,.2f}".format(value)
