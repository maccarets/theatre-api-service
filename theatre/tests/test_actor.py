from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Actor

ACTOR_URL = reverse("theatre:actor-list")

def detail_url(actor_id):
    return reverse("theatre:actor-detail", args=[actor_id])

class ActorApiViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            password="adminpass",
            email="admin@example.com"
        )
        self.client.force_authenticate(self.admin_user)
        self.actor_data = {
            "first_name": "John",
            "last_name": "Doe",

        }
        self.actor = Actor.objects.create(**self.actor_data)

    def test_list_actors(self):
        response = self.client.get(ACTOR_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_actor(self):
        response = self.client.get(detail_url(self.actor.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.actor_data["first_name"])

    def test_create_actor(self):
        new_actor_data = {
            "first_name": "Jane",
            "last_name": "Smith"

        }
        response = self.client.post(ACTOR_URL, new_actor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Actor.objects.count(), 2)

    def test_update_actor(self):
        updated_data = {
            "first_name": "Jane Updated",
            "last_name": "Smith Updated",
        }
        response = self.client.put(detail_url(self.actor.id), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.actor.refresh_from_db()
        self.assertEqual(self.actor.first_name, updated_data["first_name"])

    def test_delete_actor(self):
        response = self.client.delete(detail_url(self.actor.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Actor.objects.count(), 0)

    def test_pagination(self):
        # Create more actors to exceed the default page size
        for i in range(15):
            Actor.objects.create(
                first_name=f"first_name_test{i}",
                last_name=f"last_name_test{i}"

            )

        response = self.client.get(ACTOR_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_permission(self):
        self.client.logout()  # Log out the admin user
        response = self.client.post(ACTOR_URL, self.actor_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
