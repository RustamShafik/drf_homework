from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from materials.models import Course, Lesson, Subscription

User = get_user_model()


class MaterialsAPITestCase(TestCase):
    def setUp(self):
        self.moder_group, _ = Group.objects.get_or_create(name="Модераторы")

        self.moderator = User.objects.create(email="mod@example.com")
        self.moderator.set_password("modpass")
        self.moderator.save()
        self.moderator.groups.add(self.moder_group)

        self.user = User.objects.create(email="user@example.com")
        self.user.set_password("userpass")
        self.user.save()

        self.course = Course.objects.create(name="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Test Lesson", course=self.course, owner=self.user
        )

        self.client = APIClient()

    def test_lessons_crud_normal_user(self):
        self.client.force_authenticate(self.user)

        resp = self.client.post(
            "/materials/lessons/create/",
            {"name": "New Lesson", "course": self.course.id},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        new_lesson_id = resp.data["id"]

        resp = self.client.get("/materials/lessons/?page=1")
        self.assertEqual(resp.status_code, 200)
        ids = [item["id"] for item in resp.data["results"]]
        self.assertIn(self.lesson.id, ids)

        resp = self.client.get(f"/materials/lessons/{self.lesson.id}/")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.patch(
            f"/materials/lessons/{self.lesson.id}/update/",
            {"name": "Updated Lesson"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["name"], "Updated Lesson")

        resp = self.client.delete(f"/materials/lessons/{new_lesson_id}/delete/")
        self.assertEqual(resp.status_code, 204)

    def test_lessons_crud_moderator(self):
        self.client.force_authenticate(self.moderator)

        resp = self.client.post(
            "/materials/lessons/create/",
            {"name": "Mod Lesson", "course": self.course.id},
            format="json",
        )
        self.assertEqual(resp.status_code, 403)

        resp = self.client.patch(
            f"/materials/lessons/{self.lesson.id}/update/",
            {"name": "Mod Updated"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(f"/materials/lessons/{self.lesson.id}/delete/")
        self.assertEqual(resp.status_code, 204)

    def test_subscription_toggle_and_flag(self):
        self.client.force_authenticate(self.user)

        resp = self.client.get(f"/materials/courses/{self.course.id}/")
        self.assertFalse(resp.data["is_subscribed"])

        resp = self.client.post(
            "/materials/courses/subscribe/", {"course": self.course.id}, format="json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["message"], "Подписка добавлена")

        resp = self.client.get(f"/materials/courses/{self.course.id}/")
        self.assertTrue(resp.data["is_subscribed"])

        resp = self.client.post(
            "/materials/courses/subscribe/", {"course": self.course.id}, format="json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["message"], "Подписка удалена")

        resp = self.client.get(f"/materials/courses/{self.course.id}/")
        self.assertFalse(resp.data["is_subscribed"])


# Create your tests here.
