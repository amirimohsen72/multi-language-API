import datetime
from base64 import b64encode

from django.contrib.auth import get_user_model
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers
# from core.models import LanguageModel, SiteSetting, ShopUserDetail
from django.utils.translation import gettext as _

# from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer


# -------------------------------------------- user ------------------------------------------
# class UserCreateSerializer(DjoserUserCreateSerializer):
#     class Meta(DjoserUserCreateSerializer.Meta):
#         fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        fields = ['username', 'fullname', 'phone_number', 'profile_image', 'gender', 'birth_date', 'Address']


# -------------------------------------------- user (customer) detail and update -------------------------------------
class UserCustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'fullname', 'phone_number', 'profile_image', 'gender', 'birth_date', 'Address']
        read_only_fields = ['username', ]


class ResetPassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['phone_number', ]

    def validate(self, data):
        p_number = data['phone_number']
        # تأیید اینکه شماره تلفن وارد شده معتبر است
        if not p_number or not (len(p_number) > 1):
            raise serializers.ValidationError({'phone_number': _('enter phone number')}, )
        if not p_number.startswith('09') or len(p_number) != 11:
            raise serializers.ValidationError({'phone_number': _('phone number is not correct'), })
        user = get_user_model().objects.filter(phone_number=p_number).first()
        if user is None:
            raise serializers.ValidationError({'phone_number': _('phone number is not exist')})
        data['is_valid'] = True
        return data


class VerifyPassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['confirm_code', ]

    def validate(self, data):
        code = data['confirm_code']
        time = datetime.datetime.now() - datetime.timedelta(minutes=5)

        if not code or not (len(code) == 5):
            raise serializers.ValidationError({'massege': _('enter verify code')}, )
        usercheck = get_user_model().objects.filter(confirm_code=code, confirm_req_time__gt=time).all()

        if usercheck is None:
            raise serializers.ValidationError({'massege': _('verify code not found')})
        data['is_valid'] = True

        return data

 