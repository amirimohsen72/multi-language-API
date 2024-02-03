import datetime
from random import randint

import rest_framework.status
from django.shortcuts import render

from django.shortcuts import render, redirect

from django.utils.translation import activate

from django.contrib import messages

from django.utils.translation import gettext_lazy as _

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, ViewSet, GenericViewSet
from decouple import config
import requests
import json

from core.models import SiteSettingModel, ShopUserDetailModel
from core.api.serializers.main_data import SettingSerializers,  AboutGandomSerializers, AboutShopSerializers, MarketExtraDataSerializers
from core.filters import PublicFilter

# tst
from config import settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.decorators import action
from django.contrib.auth import get_user_model


# ------------------------------------------- user ----------------------------------------
from rest_framework.response import Response
from rest_framework import generics, mixins, status


class ExtraDataView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicFilter
    model = ShopUserDetailModel
    serializer_class = MarketExtraDataSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')
        if license_key:
            try:
                queryset = ShopUserDetailModel.objects.translated(lang).get(user_license=license_key)
                serializer = MarketExtraDataSerializers(queryset, context={'lang': lang, 'request': request})
            except ShopUserDetailModel.DoesNotExist:
                return Response({'message': _('error in get market data')}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:

                queryset = SiteSettingModel.objects.translated(lang).filter(status=True).first()
                serializer = SettingSerializers(queryset, context={'lang': lang, 'request': request})
            except SiteSettingModel.DoesNotExist:
                return Response({'message': _('error in get market data')}, status=status.HTTP_204_NO_CONTENT)

            # serializer = SettingSerializers(queryset, context={'lang': lang})

        return Response(serializer.data)



class AboutDataView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicFilter
    model = ShopUserDetailModel
    serializer_class = AboutShopSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')
        if license_key:
            try:
                queryset = ShopUserDetailModel.objects.translated(lang).get(user_license=license_key)
                serializer = AboutShopSerializers(queryset, context={'lang': lang})
            except ShopUserDetailModel.DoesNotExist:
                return Response({'message': _('error in get shop data')}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:

                queryset = SiteSettingModel.objects.translated(lang).filter(status=True).first()
                serializer = AboutShopSerializers(queryset, context={'lang': lang})
            except SiteSettingModel.DoesNotExist:
                return Response({'message': _('error in get shop data')}, status=status.HTTP_204_NO_CONTENT)

            # serializer = AboutGandomSerializers(queryset, context={'lang': lang})

        return Response(serializer.data)

