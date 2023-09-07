from rest_framework.routers import DefaultRouter
from store.views import CategoryViewSet, BookViewSet, CustomerViewSet, OrderViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('books', BookViewSet)
router.register('customers', CustomerViewSet, basename='customer')
router.register('orders', OrderViewSet)

urlpatterns = router.urls
