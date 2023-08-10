from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import ActorApiViewSet

router = DefaultRouter()
router.register("actors", ActorApiViewSet)
urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
