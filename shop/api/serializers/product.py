from decimal import Decimal
from django.utils.text import slugify
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers
from django.db import transaction

from shop.models import ProductModel, FavoriteProductModel
from .product_image import ProductImageSerializer
from .category import CategoryInProductDetailSerializers


class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductModel)

    class Meta:
        model = ProductModel
        fields = ['translations', 'id', 'image', 'get_type_display', ]

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
            'type': super().to_representation(instance)['get_type_display'],

        }
        return data


# ------------------------------------product detail ---------------------------------------
class ProductDetailSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductModel)
    images = serializers.SerializerMethodField()
    category = CategoryInProductDetailSerializers(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ['translations', 'id', 'images', 'category',
                  'get_type_display', 'is_favorite', 'is_saved']

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')
        data = {
            'title': super().to_representation(instance)['translations'][lang]['title'],
            'description': super().to_representation(instance)['translations'][lang]['description'],
            'slug': super().to_representation(instance)['translations'][lang]['slug'],
            'size': super().to_representation(instance)['translations'][lang]['size'] if
            super().to_representation(instance)['translations'][lang]['size'] else None,
            'carat': super().to_representation(instance)['translations'][lang]['carat'],
            'weight': super().to_representation(instance)['translations'][lang]['weight'],
            'price': super().to_representation(instance)['translations'][lang]['price'],
            'id': super().to_representation(instance)['id'],
            'category': super().to_representation(instance)['category'],
            'type': super().to_representation(instance)['get_type_display'],
            'images': self.get_images(instance),
            'isFavorite': self.get_is_favorite(instance),
            'isSaved': self.get_is_saved(instance),
        }

        return data

    def get_images(self, obj):
        return ProductImageSerializer(instance=obj.all_images, many=True, context=self.context).data

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FavoriteProductModel.objects.filter(product__id=obj.id, user=request.user).exists()
        else:
            return False
