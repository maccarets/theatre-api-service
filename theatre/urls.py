from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import (
    ActorApiViewSet,
    GenreApiViewSet,
    PlayApiViewSet,
    PerformanceApiViewSet,
    TheatreHallApiViewSet,
    ReservationApiViewSet,
)

router = DefaultRouter()
router.register("actors", ActorApiViewSet)
router.register("genres", GenreApiViewSet)
router.register("plays", PlayApiViewSet)
router.register("performances", PerformanceApiViewSet)
router.register("theatre_halls", TheatreHallApiViewSet)
router.register("reservations", ReservationApiViewSet)

urlpatterns = router.urls

app_name = "theatre"
