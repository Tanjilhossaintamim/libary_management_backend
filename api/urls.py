from rest_framework.routers import DefaultRouter
from store.views import CategoryViewSet, BookViewSet, CustomerViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('books', BookViewSet)
router.register('customers', CustomerViewSet)

urlpatterns = router.urls
