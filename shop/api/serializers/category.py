from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from shop.models import CategoryModel

class CategorySerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CategoryModel)

    class Meta:
        model = CategoryModel
        fields = [
            'cover',
            'id',
            'translations',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'description': super().to_representation(instance)['translations'][lang]['description'],
            'slug': super().to_representation(instance)['translations'][lang]['slug'],
            'cover': super().to_representation(instance)['cover'],
            'id': super().to_representation(instance)['id'],
        }

        return data


# ---------------------------------------- category in detail ----------------------------------------------------
class CategoryInProductDetailSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CategoryModel)

    class Meta:
        model = CategoryModel
        fields = [
            'translations','id',
        ]

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'slug': super().to_representation(instance)['translations'][lang]['slug'],
            'id': super().to_representation(instance)['id'],

        }
        return data
