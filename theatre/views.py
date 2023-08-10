from django.shortcuts import render
from rest_framework import generics, viewsets

from theatre.models import Actor, Genre, Play, Performance, TheatreHall
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayDetailSerializer,
    PerformanceDetailSerializer,
    PerformanceSerializer,
    TheatreHallSerializer,
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
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


class PerformanceApiViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer
