from datetime import datetime

from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from theatre.models import Actor, Genre, Play, Performance, TheatreHall, Reservation
from theatre.permissions import IsAdminOrReadOnly
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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class ActorApiViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrReadOnly,)


class GenreApiViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrReadOnly,)


class TheatreHallApiViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrReadOnly,)


class PlayApiViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return PlayDetailSerializer
        return PlaySerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.prefetch_related("genres", "actors")
        title = self.request.query_params.get("title")

        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=OpenApiTypes.INT,
                description="Filter by title id (ex. ?title=2)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PerformanceApiViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return PerformanceListSerializer
        return PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related("play", "theatre_hall")

        date = self.request.query_params.get("date")
        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by datetime of Performance (ex. ?date=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationApiViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Reservation.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user).prefetch_related(
            "tickets",
            "tickets__performance__play",
            "tickets__performance__theatre_hall",
        )

        # if self.action == "list":
        #     queryset.prefetch_related(
        #         "tickets__performance__play", "tickets__performance__theatre_hall"
        #     )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
