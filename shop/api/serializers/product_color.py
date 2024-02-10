from rest_framework import serializers

from shop.models import ProductColor


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'color_code', 'color_name']
