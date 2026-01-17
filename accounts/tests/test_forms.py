from django.test import TestCase
from accounts.forms import WorkerRegistrationForm

class WorkerRegistrationFormTest(TestCase):
    def test_form_valid(self):
        form = WorkerRegistrationForm(data={
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertTrue(form.is_valid())