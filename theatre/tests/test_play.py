from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from theatre.models import Play, Genre, Actor
from theatre.serializers import PlayDetailSerializer
from theatre.views import PlayApiViewSet

PLAY_URL = reverse("theatre:play-list")

def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])

class PlayApiViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            password="adminpass",
            email="admin@example.com"
        )
        self.client.force_authenticate(self.admin_user)
        self.genre = Genre.objects.create(name="Drama")
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.play_data = {
            "title": "Hamlet",
            "description": "A classic tragedy",
        }

        self.play = Play.objects.create(**self.play_data)
        self.play.genres.set([self.genre])
        self.play.actors.set([self.actor])
    def test_list_plays(self):
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_play(self):
        response = self.client.get(detail_url(self.play.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.play_data["title"])
        self.assertEqual(response.data["description"], self.play_data["description"])

    def test_create_play(self):
        new_play_data = {
            "title": "Romeo and Juliet",
            "description": "A romantic tragedy",
            "genres": [self.genre.id],
            "actors": [self.actor.id],
        }
        response = self.client.post(PLAY_URL, new_play_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Play.objects.count(), 2)

    def test_update_play(self):
        updated_data = {
            "title": "Updated Play",
            "description": "An updated description",
            "genres": [self.genre.id],
            "actors": [self.actor.id],
        }
        response = self.client.put(detail_url(self.play.id), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.play.refresh_from_db()
        self.assertEqual(self.play.title, updated_data["title"])
        self.assertEqual(self.play.description, updated_data["description"])

    def test_delete_play(self):
        response = self.client.delete(detail_url(self.play.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Play.objects.count(), 0)

    def test_serializer_class_retrieve(self):
        view = PlayApiViewSet()
        view.action = "retrieve"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PlayDetailSerializer)

    def test_serializer_class_list(self):
        view = PlayApiViewSet()
        view.action = "list"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PlayDetailSerializer)

    def test_filter_by_title(self):
        response = self.client.get(PLAY_URL, {"title": "Hamlet"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_pagination(self):
        # Create more plays to exceed the default page size
        for i in range(15):
            Play.objects.create(
                title=f"Play {i}",
                description="A play"
            )

        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_permission(self):
        self.client.logout()  # Log out the admin user
        response = self.client.post(PLAY_URL, self.play_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
