from django.shortcuts import render
from rest_framework import generics, viewsets, mixins

from theatre.models import Actor, Genre, Play, Performance, TheatreHall, Reservation
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayDetailSerializer,
    PerformanceSerializer,
    TheatreHallSerializer,
    ReservationSerializer,
    ReservationListSerializer,
    PerformanceListSerializer,
)


# Create your views here.
class ActorApiViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreApiViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TheatreHallApiViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayApiViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return PlayDetailSerializer
        return PlaySerializer


class PerformanceApiViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return PerformanceListSerializer
        return PerformanceSerializer


class ReservationApiViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)