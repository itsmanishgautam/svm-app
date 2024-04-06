from django import template


register = template.Library()

# @register.filter('hindi_int')
# def hindi_int(english_int):
#     devanagari_nums = ('०','१','२','३','४','५','६','७','८','९')
#     number = str(english_int)
#     return ''.join(devanagari_nums[int(digit)] for digit in number)


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.simple_tag
def paginate_url(value,field_name,urlencode=None):
    url = "?{}={}".format(field_name,value)

    if urlencode:
        #if url has query parameters of filter, it is in urlencode
        # splitting the urlencode at & so that parameters gets separated
        querystring = urlencode.split('&')
        # filtering page parameter from the list
        filtered_querystring = filter(lambda q:q.split('=')[0]!=field_name,querystring)
        #again encoding the list with &
        encoded_querystring = '&'.join(filtered_querystring)
        # joining page parameter with encoded list
        url = '{}&{}'.format(url,encoded_querystring)
    
    return url