from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import ActorApiViewSet, GenreApiViewSet, PlayApiViewSet

router = DefaultRouter()
router.register("actors", ActorApiViewSet)
router.register("genre", GenreApiViewSet)
router.register("play", PlayApiViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
