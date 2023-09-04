from rest_framework.routers import DefaultRouter
from store.views import CategoryViewSet, BookViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('books', BookViewSet)

urlpatterns = router.urls
