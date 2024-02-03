import datetime
from base64 import b64encode

from django.contrib.auth import get_user_model
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers
from core.models import LanguageModel, SiteSettingModel, ShopUserDetailModel
from django.utils.translation import gettext as _

# from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
# from djoser.serializers import UserSerializer as DjoserUserSerializer

 
# ----------------------------------------------- app setting detail ----------------------------------------------

class SettingSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SiteSettingModel)

    # cover = serializers.ImageField(use_url=True)

    class Meta:
        model = SiteSettingModel
        fields = [
            'favicon',
            'translations',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'site_logo': super().to_representation(instance)['translations'][lang]['site_logo'],
            'footer_description': super().to_representation(instance)['translations'][lang]['footer_description'],
            'mobile': super().to_representation(instance)['translations'][lang]['mobile'],
            'support_phone': super().to_representation(instance)['translations'][lang]['support_phone'],
            'email': super().to_representation(instance)['translations'][lang]['email'],
            'favicon': super().to_representation(instance)['favicon'],
        }

        return data


# -----------------------------------------------about gandom ----------------------------------------
class AboutGandomSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SiteSettingModel)

    # cover = serializers.ImageField(use_url=True)

    class Meta:
        model = SiteSettingModel
        fields = [
            'translations',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'about_gandom': super().to_representation(instance)['translations'][lang]['about_gandom'],
        }

        return data


# -----------------------------------------------about gandom ----------------------------------------
class AboutShopSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ShopUserDetailModel)

    class Meta:
        model = ShopUserDetailModel
        fields = [
            'translations',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        print(lang)
        data = {
            'about_gandom': super().to_representation(instance)['translations'][lang]['about_gandom'],
        }

        return data


# ------------------------------------------------ market extra data ----------------------------------

class MarketExtraDataSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ShopUserDetailModel)

    # cover = serializers.ImageField(use_url=True)

    class Meta:
        model = ShopUserDetailModel
        fields = [
            'translations',
            'user_license',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'app_logo': super().to_representation(instance)['translations'][lang]['app_logo'],
            'footer_description': super().to_representation(instance)['translations'][lang]['footer_description'],
            'mobile': super().to_representation(instance)['translations'][lang]['mobile'],
            'support_phone': super().to_representation(instance)['translations'][lang]['support_phone'],
            'email': super().to_representation(instance)['translations'][lang]['email'],
            'license_key': super().to_representation(instance)['user_license'],
        }

        return data
