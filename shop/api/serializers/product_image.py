from rest_framework import serializers


class ProductImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
