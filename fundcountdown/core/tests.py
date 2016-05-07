from django.test import TestCase


class CoreTest(TestCase):

    def test_homepage_access(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_admin_access(self):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 301)
