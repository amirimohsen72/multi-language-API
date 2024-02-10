from django.shortcuts import render

from rest_framework import generics, response

from shop.api.serializers.category import CategorySerializers

from shop.models import CategoryModel


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializers

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        return CategoryModel.objects.translated(lang).filter(status=True).all()

    def get(self, request, *args, **kwargs):
        """"
        get list of category in home
        """
        lang = self.request.query_params.get('lang', 'en')
        data = CategoryModel.objects.translated(lang).filter(status=True).all()
        return response.Response(self.serializer_class(instance=data, many=True, context={'lang': lang,'request':request}).data)
