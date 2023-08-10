from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import (
    ActorApiViewSet,
    GenreApiViewSet,
    PlayApiViewSet,
    PerformanceApiViewSet,
)

router = DefaultRouter()
router.register("actors", ActorApiViewSet)
router.register("genres", GenreApiViewSet)
router.register("plays", PlayApiViewSet)
router.register("performance", PerformanceApiViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
