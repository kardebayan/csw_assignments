from datetime import timedelta

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


class PostDetailSimilarPostsTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username='author',
            password='testpass123',
        )
        now = timezone.now()
        self.post = self.create_post('Main Post', 'main-post', now)
        self.post.tags.add('django', 'python', 'web')

        self.three_shared = self.create_post(
            'Three Shared Tags',
            'three-shared-tags',
            now - timedelta(days=1),
        )
        self.three_shared.tags.add('django', 'python', 'web')

        self.two_shared = self.create_post(
            'Two Shared Tags',
            'two-shared-tags',
            now - timedelta(days=2),
        )
        self.two_shared.tags.add('django', 'python')

        self.one_shared_newer = self.create_post(
            'One Shared Tag Newer',
            'one-shared-tag-newer',
            now - timedelta(hours=1),
        )
        self.one_shared_newer.tags.add('django')

        self.one_shared_older = self.create_post(
            'One Shared Tag Older',
            'one-shared-tag-older',
            now - timedelta(days=3),
        )
        self.one_shared_older.tags.add('python')

        self.fifth_match = self.create_post(
            'Fifth Similar Post',
            'fifth-similar-post',
            now - timedelta(days=4),
        )
        self.fifth_match.tags.add('web')

        self.unrelated = self.create_post(
            'Unrelated Post',
            'unrelated-post',
            now - timedelta(days=5),
        )
        self.unrelated.tags.add('css')

        self.draft = self.create_post(
            'Draft Similar Post',
            'draft-similar-post',
            now - timedelta(minutes=30),
            status=Post.Status.DRAFT,
        )
        self.draft.tags.add('django', 'python', 'web')

    def create_post(self, title, slug, publish, status=Post.Status.PUBLISHED):
        return Post.objects.create(
            title=title,
            slug=slug,
            body=f'{title} body.',
            publish=publish,
            status=status,
            author=self.author,
        )

    def test_detail_page_shows_ranked_limited_similar_posts(self):
        response = self.client.get(self.post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        similar_posts = list(response.context['similar_posts'])
        self.assertEqual(
            [post.title for post in similar_posts],
            [
                'Three Shared Tags',
                'Two Shared Tags',
                'One Shared Tag Newer',
                'One Shared Tag Older',
            ],
        )
        self.assertContains(response, 'Similar Posts')
        self.assertContains(response, self.three_shared.title)
        self.assertNotIn(self.post, similar_posts)
        self.assertNotContains(response, self.unrelated.title)
        self.assertNotContains(response, self.draft.title)
        self.assertNotContains(response, self.fifth_match.title)
