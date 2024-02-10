from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from shop.api.serializers.category import CategoryInProductDetailSerializers
from shop.models import FavoriteProductModel, ProductModel


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProductModel
        fields = ('product',)

    def validate_product(self, value):
        product = ProductModel.objects.get(pk=value)
        if product is None:
            raise serializers.ValidationError({
                'product': 'Product not found.',
            })
        return value

    # def validate_user(self, value):
    #     user = self.context['request'].user
    #     if user is None:
    #         raise serializers.ValidationError({
    #             'user': 'User not found.',
    #         })
    #     return value


class ProductInFavoriteSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductModel)
    category = CategoryInProductDetailSerializers(many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = ['translations', 'brand', 'id', 'image', 'colors', 'category']

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'slug': super().to_representation(instance)['translations'][lang]['slug'],
            'size': super().to_representation(instance)['translations'][lang]['size'] if
            super().to_representation(instance)['translations'][lang]['size'] else None,
            'carat': super().to_representation(instance)['translations'][lang]['carat'],
            'weight': super().to_representation(instance)['translations'][lang]['weight'],
            'price': super().to_representation(instance)['translations'][lang]['price'],
            'id': super().to_representation(instance)['id'],
            'image': super().to_representation(instance)['image'],
            'category': super().to_representation(instance)['category'],

        }
        return data


class FavoriteProductListSerializers(serializers.ModelSerializer):
    products = ProductInFavoriteSerializer(source='product', read_only=True)

    class Meta:
        model = FavoriteProductModel
        fields = [
            'products',
        ]
