from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import TheatreHall

THEATRE_HALL_URL = reverse("theatre:theatrehall-list")

def detail_url(theatre_hall_id):
    return reverse("theatre:theatrehall-detail", args=[theatre_hall_id])

class TheatreHallApiViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            password="adminpass",
            email="admin@example.com"
        )
        self.client.force_authenticate(self.admin_user)
        self.theatre_hall_data = {
            "name": "Main Hall",
            "rows": 10,
            "seats_in_row": 20,
        }
        self.theatre_hall = TheatreHall.objects.create(**self.theatre_hall_data)

    def test_list_theatre_halls(self):
        response = self.client.get(THEATRE_HALL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_theatre_hall(self):
        response = self.client.get(detail_url(self.theatre_hall.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.theatre_hall_data["name"])

    def test_create_theatre_hall(self):
        new_theatre_hall_data = {
            "name": "Small Hall",
            "rows": 5,
            "seats_in_row": 15,
        }
        response = self.client.post(THEATRE_HALL_URL, new_theatre_hall_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TheatreHall.objects.count(), 2)

    def test_update_theatre_hall(self):
        updated_data = {
            "name": "Updated Hall",
            "rows": 12,
            "seats_in_row": 18,
        }
        response = self.client.put(detail_url(self.theatre_hall.id), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.theatre_hall.refresh_from_db()
        self.assertEqual(self.theatre_hall.name, updated_data["name"])

    def test_delete_theatre_hall(self):
        response = self.client.delete(detail_url(self.theatre_hall.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TheatreHall.objects.count(), 0)

    def test_capacity_calculation(self):
        self.assertEqual(self.theatre_hall.capacity, 10 * 20)

    def test_permission(self):
        self.client.logout()  # Log out the admin user
        response = self.client.post(THEATRE_HALL_URL, self.theatre_hall_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
