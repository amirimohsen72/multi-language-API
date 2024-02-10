from django.urls import path
from .views import *

app_name = 'shop'
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('product_list', ProductViewSet, basename='product_list')
router.register('home_search', HomeSearchView, basename='home_search')
router.register('carts', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='order')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', CartItemViewSet, basename='cart-items')
# router.register('category_products', ProductCatViewSet, basename='category_product')

urlpatterns = router.urls + cart_items_router.urls

urlpatterns += [
    path('news/', NewsView.as_view(), name='newsView'),
    path('category/', CategoryView.as_view(), name='categoryView'),
    path('brand/', BrandView.as_view(), name='brandView'),
    path('products/newest/', NewestProductView.as_view(), name='newest_products'),
    # path('products/cat_newest/', CatNewestProductView.as_view(), name='newest_products'),
    path('products/cat_level_one/', CatlevelOneProductView.as_view(), name='Lvl1_products'),
    path('products/cat_level_high/', CatlevelHighProductView.as_view(), name='Lvl_high_products'),
    path('products/cat_level_luxury/', CatLuxuryProductView.as_view(), name='Luxury_products'),

    # path('products/home_search', HomeSearchView.as_view, name='home_search_product'),
    path('favorite-products/', FavoriteProductSubmitView.as_view()),
    path('pending_purchase/', PendingPurchaseSubmitView.as_view(),name='purchase_list'),
    # path('pending_purchase/remove/', PendingPurchaseRemoveView.as_view(),name='purchase_list_remove'),

    # path('home/', HomeAPIView.as_view(), name='homeview'),
]
