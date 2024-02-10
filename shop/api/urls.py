from rest_framework_nested import routers
from django.urls import path
from .views import *

app_name = 'shop'

router = routers.DefaultRouter()
router.register('product_list', ProductViewSet, basename='product_list')
router.register('home_search', HomeSearchView, basename='home_search')

urlpatterns = router.urls

urlpatterns += [
    path('news/', NewsView.as_view(), name='newsView'),
    path('category/', CategoryView.as_view(), name='categoryView'),

    path('products/newest/', NewestProductView.as_view(), name='newest_products'),
    path('products/cat_level_one/',
         CatlevelOneProductView.as_view(), name='Lvl1_products'),
    path('products/cat_level_high/',
         CatlevelHighProductView.as_view(), name='Lvl_high_products'),
    path('products/cat_level_luxury/',
         CatLuxuryProductView.as_view(), name='Luxury_products'),

    path('favorite-products/', FavoriteProductSubmitView.as_view()),
]
