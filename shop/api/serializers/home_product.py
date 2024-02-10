from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from shop.models import ProductModel
from rest_framework import serializers


class HomeProductSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductModel)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductModel
        fields = [
            'image',
            'id',
            'translations',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'description': super().to_representation(instance)['translations'][lang]['description'],
            'slug': super().to_representation(instance)['translations'][lang]['slug'],
            'price': super().to_representation(instance)['translations'][lang]['price'],
            'carat': super().to_representation(instance)['translations'][lang]['carat'],
            'weight': super().to_representation(instance)['translations'][lang]['weight'],
            'image': super().to_representation(instance)['image'],
            'id': super().to_representation(instance)['id'],
        }
        return data
