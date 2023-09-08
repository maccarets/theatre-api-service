from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Genre

GENRE_URL = reverse("theatre:genre-list")

def detail_url(genre_id):
    return reverse("theatre:genre-detail", args=[genre_id])

class GenreApiViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            password="adminpass",
            email="admin@example.com"
        )
        self.client.force_authenticate(self.admin_user)
        self.genre_data = {
            "name": "Drama",
        }
        self.genre = Genre.objects.create(**self.genre_data)

    def test_list_genres(self):
        response = self.client.get(GENRE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_genre(self):
        response = self.client.get(detail_url(self.genre.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.genre_data["name"])

    def test_create_genre(self):
        new_genre_data = {
            "name": "Comedy",
        }
        response = self.client.post(GENRE_URL, new_genre_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)

    def test_update_genre(self):
        updated_data = {
            "name": "Drama Updated",
        }
        response = self.client.put(detail_url(self.genre.id), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, updated_data["name"])

    def test_delete_genre(self):
        response = self.client.delete(detail_url(self.genre.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)

    def test_pagination(self):
        # Create more genres to exceed the default page size
        for i in range(15):
            Genre.objects.create(
                name=f"Genre{i}",
            )

        response = self.client.get(GENRE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_permission(self):
        self.client.logout()  # Log out the admin user
        response = self.client.post(GENRE_URL, self.genre_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
