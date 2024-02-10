from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from rest_framework import serializers

from shop.models import NewsModel


class NewsSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=NewsModel)
    cover = serializers.ImageField(use_url=True)

    class Meta:
        model = NewsModel
        fields = [
            'cover',
            'translations',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'description': super().to_representation(instance)['translations'][lang]['description'],
            'cover': super().to_representation(instance)['cover'],
        }

        return data
