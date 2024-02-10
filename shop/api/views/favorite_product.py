# وییو
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from shop.models import FavoriteProductModel, ProductModel
from shop.api.serializers.favorite_product import FavoriteProductSerializer, FavoriteProductListSerializers, \
    ProductInFavoriteSerializer


class FavoriteProductSubmitView(GenericAPIView):
    model = FavoriteProductModel
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        user = request.user
        product = get_object_or_404(ProductModel, pk=product_id)
        try:
            favorite_product = FavoriteProductModel.objects.get(
                product=product, user=user
            )
            favorite_product.delete()
            return Response({'message': _('The product has been removed from your favorites')},
                            status=status.HTTP_204_NO_CONTENT)
        except FavoriteProductModel.DoesNotExist:
            favorite_product = FavoriteProductModel(
                product=product, user=user
            )
            favorite_product.save()
            return Response({'message': _('The product has been added to your favorites')},
                            status=status.HTTP_201_CREATED)

        return Response(favorite_product.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        favorite = FavoriteProductModel.objects.filter(user=user).values('product_id')
        queryset = ProductModel.objects.filter(id__in=favorite)
        lang = self.request.query_params.get('lang', 'en')
        # serializer1 = FavoriteProductListSerializers(queryset, many=True, context={'lang': lang, 'request': request})
        serializer1 = ProductInFavoriteSerializer(queryset, many=True, context={'lang': lang, 'request': request})

        return Response(serializer1.data)

    def get_queryset(self):
        return FavoriteProductModel.objects.all()
