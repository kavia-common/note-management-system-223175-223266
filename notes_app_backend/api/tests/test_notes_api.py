from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Note


class NoteModelTests(APITestCase):
    def test_note_tag_list(self):
        note = Note.objects.create(title="T", content="C", tags="a,b, c , ,d", archived=False)
        self.assertEqual(note.tag_list(), ["a", "b", "c", "d"])


class NoteApiTests(APITestCase):
    def setUp(self):
        Note.objects.create(title="Hello", content="World", tags="greet,world", archived=False)
        Note.objects.create(title="Archived", content="Yes", tags="old", archived=True)

    def test_health(self):
        url = reverse("Health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})

    def test_list_notes(self):
        url = reverse("note-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_create_note(self):
        url = reverse("note-list-create")
        payload = {
            "title": "New",
            "content": "Body",
            "tags": ["new", "api"],
            "archived": False,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data["tags"]), {"new", "api"})

    def test_retrieve_update_delete_note(self):
        note = Note.objects.create(title="X", content="Y", tags="x,y", archived=False)
        detail_url = reverse("note-detail", kwargs={"pk": note.id})

        # retrieve
        r = self.client.get(detail_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["title"], "X")

        # patch
        r = self.client.patch(detail_url, {"archived": True}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertTrue(r.data["archived"])

        # put
        r = self.client.put(detail_url, {"title": "Z", "content": "ZC", "tags": ["z"], "archived": False}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["title"], "Z")

        # delete
        r = self.client.delete(detail_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_filtering(self):
        url = reverse("note-list-create")
        # search q
        r = self.client.get(url, {"q": "hello"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(r.data["results"]), 1)

        # archived
        r = self.client.get(url, {"archived": "true"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        for item in r.data["results"]:
            self.assertTrue(item["archived"])

        # tag filter
        r = self.client.get(url, {"tag": "world"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(r.data["results"]), 1)
