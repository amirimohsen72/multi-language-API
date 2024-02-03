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

from core.models import LanguageModel, SiteSettingModel, ShopUserDetailModel
from core.api.serializers.language import LanguageSerializer

from core.filters import PublicFilter

# tst
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
    queryset = LanguageModel.objects.all().order_by('sort')

