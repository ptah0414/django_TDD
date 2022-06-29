from django.test import TestCase
from django.urls import resolve
from board.views import create


class TestUrls(TestCase):
    def test_create_url_is_resolved(self):
        url = resolve('/board/create')
        self.assertEqual(url.func, create)
