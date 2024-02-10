from django.shortcuts import render

from rest_framework import generics, response

from shop.api.serializers.news import NewsSerializers

from shop.models import NewsModel


# from utils.versioning import BaseVersioning
# from utils.paginations import BasePagination


class NewsView(generics.ListAPIView):
    serializer_class = NewsSerializers

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        return NewsModel.objects.translated(lang).filter(status='1').all()[:5]

    def get(self, request, *args, **kwargs):
        """"
        get list of news cover
        """
        lang = self.request.query_params.get('lang', 'en')
        data = NewsModel.objects.translated(lang).filter(status='1').all()[:5]
        return response.Response(self.serializer_class(instance=data, many=True, context={'lang': lang,'request': request}).data)
