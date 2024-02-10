from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from shop.api.serializers.category import CategorySerializers
from shop.api.serializers.home import HomeSerializers
from shop.models import CategoryModel


class HomeAPIView(APIView):
    """
    home page api
    """
    # authentication_classes = [authentication.TokenAuthentication]

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        show all data to request for home page
        """
        lang = self.request.query_params.get('lang', None)

        # print('get:'+lang)
        # serializer = CategorySerializers(.objects.all(), manCategoryModely=True)
        serializer = HomeSerializers(context={'lang': lang}, )
        # print(serializer)
        # usernames = [user.username for user in User.objects.all()]
        return Response(serializer.data)
