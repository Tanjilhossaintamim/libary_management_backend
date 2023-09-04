from rest_framework.routers import DefaultRouter
from store.views import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = router.urls
