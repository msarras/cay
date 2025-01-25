from django.utils import translation
from django.shortcuts import redirect

def switch_language(request, lang_code):
    translation.activate(lang_code)
    request.session['django_language'] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))
