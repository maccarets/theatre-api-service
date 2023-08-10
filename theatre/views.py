from django.shortcuts import render
from rest_framework import generics, viewsets

from theatre.models import Actor, Genre, Play
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayDetailSerializer,
)


# Create your views here.
class ActorApiViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreApiViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayApiViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer
