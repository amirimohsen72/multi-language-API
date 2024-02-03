import datetime
from base64 import b64encode

from django.contrib.auth import get_user_model
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers
from core.models import LanguageModel 
from django.utils.translation import gettext as _

# from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer



# -------------------------------------------- languages -------------------------------------
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = ['title', 'lang_code', 'lang_logo', 'image', ]

    image = serializers.ImageField(source='lang_logo', help_text='base64 image')

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Change the display name of the "lang_code" field
        image_data = b64encode(instance.lang_logo.read())
        instance.lang_logo.seek(0)
        data['image'] = image_data
        return data
 