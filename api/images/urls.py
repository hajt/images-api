from rest_framework import routers

from .views import ImageViewSet


iamges_router = routers.SimpleRouter()
iamges_router.register("images", ImageViewSet, basename="images")

urlpatterns = iamges_router.urls
