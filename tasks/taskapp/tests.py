from django.test import TestCase
from .models import Task

class TaskTests(TestCase):
    def test_create_task(self):
        task = Task.objects.create(title="Test task", status="new")
        self.assertEqual(task.status, "new")