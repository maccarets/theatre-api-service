from django.db import models
from rest_framework.exceptions import ValidationError

from user.models import User


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="plays")
    actors = models.ManyToManyField(Actor, related_name="plays")

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, theatre_hall, error_to_raise):
        for ticket_attr_value, ticket_attr_name, theatre_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row")
        ]:
            count_attr = getattr(theatre_hall, theatre_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attr):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range:"
                                          f"(1, {theatre_hall_attr_name})"
                                          f"(1, {count_attr}"

                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.performance.theatre_hall,
            ValidationError
        )
