from django.shortcuts import render
from rest_framework import generics, viewsets

from theatre.models import Actor
from theatre.serializers import ActorSerializer


# Create your views here.
class ActorApiViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
