from rest_framework import serializers

from shop.models import CategoryModel

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from shop.api.serializers.home_product import HomeProductSerializers


class CategoryProductSerializers(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CategoryModel)
    products = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModel
        fields = (
            'id',
            'translations',
            'products',
        )

    def get_products(self, obj):
        return HomeProductSerializers(instance=obj.products.all()[:10], many=True,
                                  context=self.context).data

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = super().to_representation(instance)['translations'][lang]
        data['products'] = [
            {
                'title': attr['title'],
                'image': attr['image'],
                'price': attr['price'],
                'carat': attr['carat'],
                'weight': attr['weight'],
                'slug': attr['slug'],
            }
            for attr in super().to_representation(instance)['products']
        ]
        return data
