from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import MyCustomUser

class AccountsViewsTestCase(TestCase):

    def setUp(self):
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.change_password_url = reverse('accounts:change_password')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.custom_user = MyCustomUser.objects.create(user=self.user)

    def test_signup_view_success(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('base:home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(MyCustomUser.objects.filter(user__username='newuser').exists())
    def test_signup_view_failure(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',  # Existing username
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    def test_login_view_success(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('base:home'))

    def test_login_view_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertFormError(response, 'form', None, ['Please enter a correct username and password. Note that both fields may be case-sensitive.'])

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('base:home'))

    def test_change_password_view_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.change_password_url, {
            'old_password': 'testpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('base:home'))

    def test_change_password_view_failure(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.change_password_url, {
            'old_password': 'wrongpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertFormError(response, 'form', 'old_password', ['Your old password was entered incorrectly. Please enter it again.'])
