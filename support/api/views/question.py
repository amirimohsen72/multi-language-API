from rest_framework.viewsets import ReadOnlyModelViewSet

from support.api.serializers.question import QuestionSerializers

from support.models import QuestionModel

from support.paginations import DefaultPagination


class QuestionView(ReadOnlyModelViewSet):
    serializer_class = QuestionSerializers
    pagination_class = DefaultPagination

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        queryset = QuestionModel.objects.translated(lang).filter(status='1').order_by('sort', 'datetime_created').all()
        return queryset

    def get_serializer_context(self):
        lang = self.request.query_params.get('lang', 'en')
        return {'request': self.request, 'lang': lang}
