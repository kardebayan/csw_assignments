from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class PostListByTagTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username='author',
            password='testpass123',
        )
        self.python_post = Post.published.create(
            title='Python Post',
            slug='python-post',
            body='Post about Python.',
            publish=timezone.now(),
            status=Post.Status.PUBLISHED,
            author=self.author,
        )
        self.django_post = Post.published.create(
            title='Django Post',
            slug='django-post',
            body='Post about Django.',
            publish=timezone.now(),
            status=Post.Status.PUBLISHED,
            author=self.author,
        )
        self.python_post.tags.add('python')
        self.django_post.tags.add('django')

    def test_post_list_by_tag_url_resolves_and_filters_posts(self):
        response = self.client.get(
            reverse('blog:post_list_by_tag', args=['python'])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.python_post.title)
        self.assertNotContains(response, self.django_post.title)
        self.assertEqual(response.context['tag'].slug, 'python')

    def test_invalid_tag_returns_404(self):
        response = self.client.get(
            reverse('blog:post_list_by_tag', args=['missing-tag'])
        )

        self.assertEqual(response.status_code, 404)
