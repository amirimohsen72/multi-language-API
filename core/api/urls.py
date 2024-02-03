from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
# router.register('languages', views.LanguageViewSet, basename='language')
router.register('customers', views.CustomerViewSet, basename='customer')
# router.register('password', views.ChangePassView, basename='password')

# products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# products_router.register('comments', views.CommentViewSet, basename='product-comments')

urlpatterns = router.urls
urlpatterns += [
    path('auth/reset_pass/', views.ResetPassView.as_view(), name='reset-password'),
    path('auth/verify_pass/', views.RecoveryVerifyView.as_view(), name='verify-password'),
    path('appdata/extradata/', views.ExtraDataView.as_view(), name='setting'),
    path('appdata/about/', views.AboutDataView.as_view(), name='aboutgandom'),
]
