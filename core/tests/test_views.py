from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import Task, TaskType, Position

from datetime import timedelta

User = get_user_model()

class CoreViewsTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="Dev")
        self.user = User.objects.create_user(username="testuser", password="password123", position=position)
        self.client.login(username="testuser", password="password123")

        self.task_type = TaskType.objects.create(name="Feature")
        self.task = Task.objects.create(
            name="Test Task",
            description="Test desc",
            deadline=timezone.now() + timedelta(days=1),
            task_type=self.task_type,
            priority="MEDIUM",
        )
        self.task.assignees.add(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("stats", response.context)

    def test_task_list_view(self):
        response = self.client.get(reverse("core:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_my_task_list_view(self):
        response = self.client.get(reverse("core:my-task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_detail_view(self):
        response = self.client.get(reverse("core:task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_create_view(self):
        response = self.client.post(reverse("core:task-create"), {
            "name": "New Task",
            "description": "Desc",
            "deadline": timezone.now() + timedelta(days=3),
            "priority": "HIGH",
            "task_type": self.task_type.id,
            "assignees": [self.user.id],
            "is_completed": False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        response = self.client.post(reverse("core:task-update", args=[self.task.id]), {
            "name": "Updated Task",
            "description": "Updated Desc",
            "deadline": self.task.deadline,
            "priority": "LOW",
            "task_type": self.task_type.id,
            "assignees": [self.user.id],
            "is_completed": True,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view(self):
        response = self.client.post(reverse("core:task-delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())