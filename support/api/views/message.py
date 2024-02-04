from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework.views import APIView

from support.models import TicketMessageModel
from support.api.serializers.message import UserMessageSerializer, MessagesListSerializers

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserMessagesView(GenericAPIView):
    model = TicketMessageModel
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TicketMessageModel.objects.filter(user=user).prefetch_related('answers').order_by(
            '-datetime_created')
        return queryset

    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'message': openapi.Schema(type=openapi.TYPE_STRING),
    #             'attachment': openapi.Schema(type=openapi.TYPE_FILE)
    #         }
    #     )
    # )
    def post(self, request, *args, **kwargs):
        serializer = UserMessageSerializer(data=request.data, context={'request': request, })
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = TicketMessageModel.objects.filter(user=user).prefetch_related('answers').order_by(
            '-datetime_created')


        messages = TicketMessageModel.objects.filter(user=user, status='2')
        messages.update(status='3')

        serializer1 = MessagesListSerializers(queryset, many=True, context={'request': request, })

        return Response(serializer1.data)
#
