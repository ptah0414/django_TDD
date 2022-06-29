from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from board.models import Post
from board.views import create


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user01',
            password='qwer1234!'
        )
        self.post = Post.objects.create(
            title='title1',
            contents='contents1',
            writer=self.user
        )

    def test_post_model_create(self):
        post = Post()
        post.title = 'title2'
        post.contents = 'contents'
        post.writer = self.user
        post.save()

        post = Post.objects.get(title='title2')
        self.assertEqual(post.title, 'title2')

    def test_post_model_read(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'title1')

    def test_post_model_update(self):
        post = Post.objects.get(id=1)
        post.title = 'title3'
        post.save()
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'title3')

    def test_post_model_delete(self):
        post = Post.objects.get(id=1)
        post.delete()

        self.assertFalse(Post.objects.filter(id=1).exists())
