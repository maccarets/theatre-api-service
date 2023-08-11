from rest_framework import serializers
from .models import Actor, Genre, Play, Reservation, TheatreHall, Performance, Ticket


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = "__all__"


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = "__all__"


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlaySerializer()
    theatre_hall = TheatreHallSerializer()


class PerformanceForTicketSerializer(PerformanceSerializer):
    class Meta:
        model = Performance
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    performance = PerformanceDetailSerializer()

    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(read_only=False, many=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")
