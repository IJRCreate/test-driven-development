from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_returns_correct_hmtl(self):
        response = self.client.get("/")
        self.assertContains(response, "<title>To-Do lists</title>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")
