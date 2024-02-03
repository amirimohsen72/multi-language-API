from django.utils import translation

from config import settings


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        language = request.GET.get('lang')

        if language and language in [code for code, _ in settings.LANGUAGES]:
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE


        response = self.get_response(request)

        return response
