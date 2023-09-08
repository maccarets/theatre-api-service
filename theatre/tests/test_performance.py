from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from theatre.models import Performance, Play, TheatreHall
from theatre.serializers import PerformanceSerializer, PerformanceListSerializer
from datetime import datetime

from theatre.views import PerformanceApiViewSet

PERFORMANCE_URL = reverse("theatre:performance-list")

def detail_url(performance_id):
    return reverse("theatre:performance-detail", args=[performance_id])

class PerformanceApiViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            password="adminpass",
            email="admin@example.com"
        )
        self.client.force_authenticate(self.admin_user)
        self.theatre_hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.play = Play.objects.create(title="Hamlet", description="A classic tragedy")
        self.performance_data = {
            "play": self.play,
            "theatre_hall": self.theatre_hall,
            "show_time": "2023-09-10T14:30:00Z",  # Example date and time
        }
        self.performance = Performance.objects.create(**self.performance_data)

    def test_list_performances(self):
        response = self.client.get(PERFORMANCE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_performance(self):
        response = self.client.get(detail_url(self.performance.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["play"]["title"], self.play.title)
        self.assertEqual(response.data["theatre_hall"]["name"], self.theatre_hall.name)

    def test_create_performance(self):
        new_performance_data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2023-08-11T09:03:45Z"
        }
        response = self.client.post(PERFORMANCE_URL, new_performance_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 2)

    def test_update_performance(self):
        updated_data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2023-09-12T16:00:00Z",  # Example date and time
        }
        response = self.client.put(detail_url(self.performance.id), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.performance.refresh_from_db()
        self.assertEqual(self.performance.show_time, datetime.fromisoformat(updated_data["show_time"]))

    def test_delete_performance(self):
        response = self.client.delete(detail_url(self.performance.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Performance.objects.count(), 0)

    def test_serializer_class_retrieve(self):
        view = PerformanceApiViewSet()
        view.action = "retrieve"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PerformanceListSerializer)

    def test_serializer_class_list(self):
        view = PerformanceApiViewSet()
        view.action = "list"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PerformanceListSerializer)

    def test_filter_by_date(self):
        response = self.client.get(PERFORMANCE_URL, {"date": "2023-09-10"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_pagination(self):
        # Create more performances to exceed the default page size
        for i in range(15):
            Performance.objects.create(
                play=self.play,
                theatre_hall=self.theatre_hall,
                show_time="2023-09-12T16:00:00Z"
            )

        response = self.client.get(PERFORMANCE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_permission(self):
        self.client.logout()  # Log out the admin user
        response = self.client.post(PERFORMANCE_URL, self.performance_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
