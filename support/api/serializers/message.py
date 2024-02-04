from django.db import transaction
from rest_framework import serializers, status
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from rest_framework.response import Response
from django.utils.translation import gettext as _

from support.models import TicketMessageModel, TicketAnswerModel
from django.contrib.auth import get_user_model


class UserMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TicketMessageModel
        fields = ('message', 'attachment', 'user')
        read_only_fields = ['user', ]

    def validate(self, attrs):
        message_empty = attrs.get('message') == ''
        attachment_empty = attrs.get('attachment') is None

        if message_empty and attachment_empty:
            raise serializers.ValidationError({
                'message': _('Entry of one of the text or attachment is required'),
            })

        return attrs


class MessagesReplySerializers(serializers.ModelSerializer):

    class Meta:
        model = TicketAnswerModel
        fields = [
            'message', 'datetime_created', 'attachment',
        ]


class MessagesListSerializers(serializers.ModelSerializer):
    answers = MessagesReplySerializers(many=True, read_only=True)
    attachment = serializers.FileField(use_url=True)

    class Meta:
        model = TicketMessageModel
        fields = [
            'message', 'datetime_created', 'attachment', 'readed', 'answers',
        ]
