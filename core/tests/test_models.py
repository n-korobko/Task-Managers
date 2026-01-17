from django.test import TestCase
from django.utils import timezone
from core.models import Position, Worker, TaskType, Task
from datetime import timedelta

class PositionModelTest(TestCase):
    def test_string_representation(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")


class WorkerModelTest(TestCase):
    def test_string_representation_with_position(self):
        position = Position.objects.create(name="Manager")
        worker = Worker.objects.create_user(username="testuser", password="pass123", position=position)
        self.assertEqual(str(worker), "testuser (Manager)")


class TaskTypeModelTest(TestCase):
    def test_string_representation(self):
        task_type = TaskType.objects.create(name="Bug Fix")
        self.assertEqual(str(task_type), "Bug Fix")


class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="QA")
        self.worker = Worker.objects.create_user(username="tester", password="pass123", position=self.position)
        self.task_type = TaskType.objects.create(name="Test Task")

    def test_task_creation(self):
        task = Task.objects.create(
            name="Fix login bug",
            description="Fix the login bug on the main page",
            deadline=timezone.now() + timedelta(days=2),
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )
        task.assignees.add(self.worker)

        self.assertEqual(task.name, "Fix login bug")
        self.assertIn(self.worker, task.assignees.all())
        self.assertEqual(str(task), "Fix login bug")