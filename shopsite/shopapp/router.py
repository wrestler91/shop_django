from rest_framework import routers
from .views import ItemAPIViewSet, RequestedItemApiViewSet

router = routers.SimpleRouter()
router.register(r'item', ItemAPIViewSet)
router.register(r'requested_item', RequestedItemApiViewSet)
