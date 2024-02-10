# from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _

from rest_framework import generics, response, status
from rest_framework.exceptions import ValidationError

from shop.api.serializers.brand import BrandSerializers

from shop.models import BrandModel


class BrandView(generics.ListAPIView):
    serializer_class = BrandSerializers

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')

        license_key = self.request.GET.get('license_key')
        qs = BrandModel.objects.translated(lang).filter(
            status=True,
            products__translations__language_code=lang
        )
        if license_key:
            try:
                return qs.filter(Q(products__author__shop_detail__user_license=license_key)).distinct()
            except ValidationError:
                return response.Response({'message': _('license key is not valid'), },
                                         status=status.HTTP_400_BAD_REQUEST)
        return qs.distinct()

    def get(self, request, *args, **kwargs):
        """
        get list of brands
        """
        lang = self.request.query_params.get('lang', 'en')
        # data = BrandModel.objects.translated(lang).filter(status=True).order_by('sort').all()
        try:
            data = self.get_queryset().order_by('sort')
            print(data.query)
        except:
            return response.Response({'message': _('license key is not valid'), },
                                     status=status.HTTP_400_BAD_REQUEST)
        return response.Response(
            self.serializer_class(instance=data, many=True, context={'lang': lang, 'request': request}).data)
