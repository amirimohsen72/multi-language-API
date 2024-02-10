from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions

from shop.models import ProductModel
from shop.api.serializers.product import ProductSerializer, ProductDetailSerializer
from shop.filters import ProductFilter
# from .permissions import CustomDjangoModelPermissions, IsAdminOrReadOnly, SendPrivateEmailToCustomerPermission

from shop.paginations import DefaultPagination


class ProductViewSet(ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        else:
            return ProductSerializer

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        queryset = ProductModel.objects.translated(lang).filter(active=True).all()

        return queryset

    def get_serializer_context(self):
        lang = self.request.query_params.get('lang', 'en')
        return {'request': self.request, 'lang': lang}
