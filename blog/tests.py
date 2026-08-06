from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='safe-test-password-123',
        )

    def test_password_is_hashed(self):
        self.assertNotEqual(self.user.password, 'safe-test-password-123')
        self.assertTrue(self.user.check_password('safe-test-password-123'))

    def test_login_page_is_available(self):
        response = self.client.get(reverse('blog:login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '账号登录')

    def test_user_can_log_in(self):
        response = self.client.post(
            reverse('blog:login'),
            {
                'username': 'testuser',
                'password': 'safe-test-password-123',
            },
        )

        self.assertRedirects(response, reverse('blog:blog_index'))
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            self.user.pk,
        )

    def test_invalid_password_does_not_log_in(self):
        response = self.client.post(
            reverse('blog:login'),
            {'username': 'testuser', 'password': 'wrong-password'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(response, '账号或密码不正确')

    def test_logout_requires_post_and_ends_session(self):
        self.client.force_login(self.user)

        get_response = self.client.get(reverse('blog:logout'))
        self.assertRedirects(get_response, reverse('blog:blog_index'))
        self.assertIn('_auth_user_id', self.client.session)

        post_response = self.client.post(reverse('blog:logout'))
        self.assertRedirects(post_response, reverse('blog:blog_index'))
        self.assertNotIn('_auth_user_id', self.client.session)
