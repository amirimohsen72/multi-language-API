from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from rest_framework import serializers

from shop.models import NewsModel
from .news import NewsSerializers


class HomeSerializers(serializers.Serializer):
    # querynews = NewsModel.objects.all()
    # lang = self.context.get('lang', 'en')
    news = NewsSerializers(NewsModel.objects.all(), many=True,)
    # def to_representation(self, instance):
    #     lang = self.context.get('lang', 'en')
    #     data = {
    #         'title': super().to_representation(instance)['translations'][lang]['title'],
    #         'description': super().to_representation(instance)['translations'][lang]['description'],
    #         'cover': super().to_representation(instance)['cover'],
    #     }
    #     return data
