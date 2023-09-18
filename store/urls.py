from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collection', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register(
    'reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register(
    'images', views.ProductImageViewSet, basename='product-images')
cart_items = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items.register('items', views.CartItemViewSet, basename='cart-items')
# URLConf
urlpatterns = router.urls + products_router.urls + cart_items.urls
