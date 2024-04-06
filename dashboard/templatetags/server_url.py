from django import template

register = template.Library()

@register.filter
def server_protocol(request):
    return 'https://' if request.is_secure() else 'http://'