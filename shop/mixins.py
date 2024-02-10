# from django.contrib import admin
# from django.contrib.auth import get_user_model
from rest_framework import generics


class MarketPlaceMixin(generics.ListAPIView):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        license_key = request.GET.get('license_key')

        if license_key:
            return qs.filter(author__shop_detail__license_key =license_key)
        return qs
        # return qs.filter(author=request.user)
