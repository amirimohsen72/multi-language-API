from django.urls import path
from .views import *

app_name = 'support'

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('question', QuestionView, basename='question')

urlpatterns = router.urls

urlpatterns += [
    path('message/', UserMessagesView.as_view(), name='message'),
]
