from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTest(TestCase):

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_post_success(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

        self.assertRedirects(response, reverse('core:task-list'))

    def test_register_post_invalid(self):
        response = self.client.post(reverse('register'), data={
            'username': 'user1',
            'password1': 'pass',
            'password2': 'pass2',
        })
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')