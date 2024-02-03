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

from core.models import Language, SiteSetting, ShopUserDetail
from core.serializers import LanguageSerializer, ResetPassUserSerializer, VerifyPassUserSerializer, SettingSerializers, \
    AboutGandomSerializers, AboutShopSerializers, MarketExtraDataSerializers
from core.filters import PublicFilter

# tst
from .serializers import UserSerializer, UserCustomerUpdateSerializer
from config import settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.decorators import action
from django.contrib.auth import get_user_model


# AUTH_USER_MODEL=settings.AUTH_USER_MODEL
def change_lang_web(request):
    activate(request.GET.get('lang'))
    return redirect(request.GET.get('next'))


@api_view(['GET'])
def change_lang(request):
    lang = request.GET.get('lang', 'en')
    activate(lang)
    return Response({'lang': lang}, status=rest_framework.status.HTTP_200_OK)


# ----------------------------------------  api ----------------------------------------
# ReadOnlyModelViewSet
class LanguageViewSet(ListAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all().order_by('sort')


# ------------------------------------------- user ----------------------------------------
from rest_framework.response import Response
from rest_framework import generics, mixins, status


class ResetPassView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = ResetPassUserSerializer

    def post(self, request):
        serializer = ResetPassUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data['phone_number']
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        new_password = ''.join([characters[randint(0, len(characters) - 1)] for _ in range(5)])
        # user = get_user_model().objects.get(phone_number=phone_number)
        user = get_object_or_404(get_user_model(),phone_number=phone_number )
        if user is not None:
            user.confirm_code = new_password
            user.confirm_req_time = datetime.datetime.now()
            user.save()
            # sms

            payamak_user = config('MELIPAYAMK_USER')
            payamak_pass = config('MELIPAYAMK_PASS')
            # payamak_from = config('MELIPAYAMK_FROM')
            payamak_from = ''
            payamak_text = f' کد احراز هویت وب اپلیکیشن گندم \n {new_password}'

            request_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            request_data = {
                'username': payamak_user,
                'password': payamak_pass,
                'from': payamak_from,
                'to': user.phone_number,
                'text': payamak_text,
            }
            # res= requests.post(url='https://api.zarinpal.com/pg/v4/payment/verify.json' , data=json.dumps(request_data), headers=request_header,)
            # res = requests.post(url='https://api.payamak-panel.com/post/Send.asmx',
            #                     data=json.dumps(request_data), headers=request_header, )
            # response = res.json()
            # print(response)

            # end sms
            msg = _('your new recovery code sent successfully')
            return Response({'message': msg, 'pass': new_password, 'response': request_data})
        return Response({'message': _('user not found'), })


class RecoveryVerifyView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = VerifyPassUserSerializer

    def post(self, request):
        serializer = VerifyPassUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirm_code = serializer.data['confirm_code']
        time = datetime.datetime.now() - datetime.timedelta(minutes=5)

        user = get_user_model()
        try:
            user_exist = user.objects.get(confirm_code=confirm_code, confirm_req_time__gt=time)

            user_exist.set_password(confirm_code)
            user_exist.confirm_code = None
            user_exist.confirm_req_time = None
            user_exist.save()
            msg = _('Password reset successfully')
        except user.DoesNotExist:
            msg = _('verify has error')
        return Response({'message': msg, })


class CustomerViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return get_user_model().objects.filter(pk=user.pk)

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = get_user_model().objects.get(pk=user_id)
        if request.method == 'GET':
            serializer = UserSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserCustomerUpdateSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ExtraDataView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicFilter
    model = ShopUserDetail
    serializer_class = MarketExtraDataSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')
        if license_key:
            try:
                queryset = ShopUserDetail.objects.translated(lang).get(user_license=license_key)
                serializer = MarketExtraDataSerializers(queryset, context={'lang': lang, 'request': request})
            except ShopUserDetail.DoesNotExist:
                return Response({'message': _('error in get market data')}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:

                queryset = SiteSetting.objects.translated(lang).filter(status=True).first()
                serializer = SettingSerializers(queryset, context={'lang': lang, 'request': request})
            except SiteSetting.DoesNotExist:
                return Response({'message': _('error in get market data')}, status=status.HTTP_204_NO_CONTENT)

            # serializer = SettingSerializers(queryset, context={'lang': lang})

        return Response(serializer.data)



class AboutDataView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicFilter
    model = ShopUserDetail
    serializer_class = AboutShopSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        license_key = self.request.GET.get('license_key')
        if license_key:
            try:
                queryset = ShopUserDetail.objects.translated(lang).get(user_license=license_key)
                serializer = AboutShopSerializers(queryset, context={'lang': lang})
            except ShopUserDetail.DoesNotExist:
                return Response({'message': _('error in get shop data')}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:

                queryset = SiteSetting.objects.translated(lang).filter(status=True).first()
                serializer = AboutShopSerializers(queryset, context={'lang': lang})
            except SiteSetting.DoesNotExist:
                return Response({'message': _('error in get shop data')}, status=status.HTTP_204_NO_CONTENT)

            # serializer = AboutGandomSerializers(queryset, context={'lang': lang})

        return Response(serializer.data)

