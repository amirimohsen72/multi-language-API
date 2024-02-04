from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from rest_framework import serializers

from support.models import QuestionModel


class QuestionSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=QuestionModel)

    class Meta:
        model = QuestionModel
        fields = [
            'translations',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
        }

        return data
