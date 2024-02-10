from django.shortcuts import render

from rest_framework import generics, response, status
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from shop.api.serializers.home_product import HomeProductSerializers
from shop.api.serializers.category_product import CategoryProductSerializers
from shop.models import ProductModel, CategoryModel
from shop.filters import HomeSearchFilter,HomeProductFilter


# ------------------------------------------------ newest product ------------------------------------------------------
class NewestProductView(generics.ListAPIView):
    serializer_class = HomeProductSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeProductFilter

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        return ProductModel.objects.translated(lang).filter(active=True, type='new').all().order_by(
            '-datetime_created')[
               :10]

    def get(self, request, *args, **kwargs):
        """
        get list of newest product in home
        """
        lang = self.request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')

        data = ProductModel.objects.order_by('-datetime_created').translated(lang).filter(active=True,
                                                                                          type='new')
        if license_key:
            try:
                data = data.filter(author__shop_detail__user_license=license_key)
            except:
                return response.Response({'message': _('license key is not valid'), },
                                         status=status.HTTP_400_BAD_REQUEST)

        data = data.all()[:10]
        return response.Response(
            self.serializer_class(instance=data, many=True, context={'lang': lang, 'request': request}).data)


# -------------------------------------------------- newest product by cat ------------------------------------------
# class CatNewestProductView(generics.ListAPIView):
#     serializer_class = CategoryProductSerializers
#
#     #
#     def get_queryset(self):
#         lang = self.request.query_params.get('lang', 'en')
#         return CategoryModel.objects.translated(lang).filter(status=True).all()[:1]
#
#     def get(self, request, *args, **kwargs):
#         """
#         get list of newest product in home
#         """
#         lang = self.request.query_params.get('lang', 'en')
#         data = CategoryModel.objects.translated(lang).filter(status=True).all()[:1]
#         return response.Response(self.serializer_class(instance=data, many=True, context={'lang': lang,'request': request}).data)


# ------------------------------------------------- type low level in home --------------------------------------------------
class CatlevelOneProductView(generics.ListAPIView):
    serializer_class = HomeProductSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeProductFilter

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        # return CategoryModel.objects.translated(lang).filter(status=True, pk=3).all()[:1]
        return ProductModel.objects.translated(lang).filter(active=True, type='low').all().order_by(
            '-datetime_created')[:10]

    def get(self, request, *args, **kwargs):
        """
        get list of newest product in home
        """
        lang = self.request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')

        # data = CategoryModel.objects.translated(lang).filter(status=True, pk=3).all()[:1]
        data = ProductModel.objects.order_by('-datetime_created').translated(lang).filter(active=True,
                                                                                          type='low')
        if license_key:
            try:
                data = data.filter(author__shop_detail__user_license=license_key)
            except:
                return response.Response({'message': _('license key is not valid'), },
                                         status=status.HTTP_400_BAD_REQUEST)
        data = data.all()[:10]
        return response.Response(
            self.serializer_class(instance=data, many=True, context={'lang': lang, 'request': request}).data)


# ------------------------------------------------- type high level in home --------------------------------------------------
class CatlevelHighProductView(generics.ListAPIView):
    serializer_class = HomeProductSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeProductFilter
    #
    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        # return CategoryModel.objects.translated(lang).filter(status=True, pk=4).all()[:1]
        return ProductModel.objects.translated(lang).filter(active=True, type='high').all().order_by(
            '-datetime_created')[:10]

    def get(self, request, *args, **kwargs):
        """
        get list of newest product in home
        """
        lang = self.request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')

        # data = CategoryModel.objects.translated(lang).filter(status=True, pk=4).all()[:1]
        data = ProductModel.objects.order_by('-datetime_created').translated(lang).filter(active=True,
                                                                                          type='high')
        if license_key:
            try:
                data = data.filter(author__shop_detail__user_license=license_key)
            except:
                return response.Response({'message': _('license key is not valid'), },
                                         status=status.HTTP_400_BAD_REQUEST)
        data = data.all()[:10]
        return response.Response(
            self.serializer_class(instance=data, many=True, context={'lang': lang, 'request': request}).data)


# ------------------------------------------------- type luxury in home --------------------------------------------------
class CatLuxuryProductView(generics.ListAPIView):
    serializer_class = HomeProductSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeProductFilter
    #
    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        # return CategoryModel.objects.translated(lang).filter(status=True, pk=5).all()[:1]
        return ProductModel.objects.translated(lang).filter(active=True, type='lux').all().order_by(
            '-datetime_created')[:10]

    def get(self, request, *args, **kwargs):
        """
        get list of newest product in home
        """
        lang = self.request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')

        # data = CategoryModel.objects.translated(lang).filter(status=True, pk=5).all()[:1]
        data = ProductModel.objects.order_by('-datetime_created').translated(lang).filter(active=True,
                                                                                          type='lux')
        if license_key:
            try:
                data = data.filter(author__shop_detail__user_license=license_key)
            except:
                return response.Response({'message': _('license key is not valid'), },
                                         status=status.HTTP_400_BAD_REQUEST)
        data = data.all()[:10]
        return response.Response(
            self.serializer_class(instance=data, many=True, context={'lang': lang, 'request': request}).data)


# ---------------------------------------------------------- home search products -------------------------------------


class HomeSearchView(viewsets.ViewSet):
    """
    A simple ViewSet for searching across multiple product types.
    """
    serializer_class = HomeProductSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeSearchFilter

    def list(self, request):
        lang = self.request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')

        queryset1 = ProductModel.objects.translated(lang).filter(type='new',
                                                                 translations__title__icontains=request.query_params.get(
                                                                     'search', '')).distinct()
        queryset2 = ProductModel.objects.translated(lang).filter(type='low',
                                                                 translations__title__icontains=request.query_params.get(
                                                                     'search', '')).distinct()
        queryset3 = ProductModel.objects.translated(lang).filter(type='high',
                                                                 translations__title__icontains=request.query_params.get(
                                                                     'search', '')).distinct()
        queryset4 = ProductModel.objects.translated(lang).filter(type='lux',
                                                                 translations__title__icontains=request.query_params.get(
                                                                     'search', '')).distinct()

        # if self.request.query_params.get('category'):
        cat = self.request.query_params.get('category', None)
        if cat is not None:
            queryset1 = queryset1.filter(category=cat)
        if cat is not None:
            queryset2 = queryset2.filter(category=cat)

        if cat is not None:
            queryset3 = queryset3.filter(category=cat)

        if cat is not None:
            queryset4 = queryset4.filter(category=cat)

        if license_key:
            try:
                queryset1 = queryset1.filter(author__shop_detail__user_license=license_key)
                queryset2 = queryset2.filter(author__shop_detail__user_license=license_key)
                queryset3 = queryset3.filter(author__shop_detail__user_license=license_key)
                queryset4 = queryset4.filter(author__shop_detail__user_license=license_key)
            except:
                return response.Response({'message': _('license key is not valid'), },
                                         status=status.HTTP_400_BAD_REQUEST)

        serializer1 = HomeProductSerializers(queryset1, many=True, context={'lang': lang, 'request': request})
        serializer2 = HomeProductSerializers(queryset2, many=True, context={'lang': lang, 'request': request})
        serializer3 = HomeProductSerializers(queryset3, many=True, context={'lang': lang, 'request': request})
        serializer4 = HomeProductSerializers(queryset4, many=True, context={'lang': lang, 'request': request})

        return response.Response({
            'new': serializer1.data,
            'low_lvl': serializer2.data,
            'high_lvl': serializer3.data,
            'luxury': serializer4.data,
        })
