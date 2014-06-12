from .models import Article, SubPageArticle
from ..general.time import now

from datetime import timedelta
from django.contrib.auth.models import User
from django.test import Client, TestCase

class ArticleViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        testauthor = User.objects.create(username='testuser')
        self.article = Article.objects.create(
            title='Testarticle',
            content='<p>News here</p>',
            published_date=now(),
            author=testauthor,
        )


    def test_get_article_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Testarticle' in response.content.decode('utf-8'))
        self.assertTrue('<p>News here</p>' in response.content.decode('utf-8'))


    def test_get_article_details(self):
        response = self.client.get('/articles/%d/' % self.article.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Testarticle' in response.content.decode('utf-8'))
        self.assertTrue('<p>News here</p>' in response.content.decode('utf-8'))


class SubPageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        testauthor = User.objects.create(username='testuser')
        self.article = SubPageArticle.objects.create(
            slug='testarticle',
            title='Test subpage',
            content='<p>Test subpage</p>',
            published_date=now(),
            author=testauthor,
        )


    def test_subpage_on_frontpage(self):
        response = self.client.get('/')
        self.assertTrue('Test subpage' in response.content.decode('utf-8'))


    def test_get_subpage(self):
        response = self.client.get('/testarticle')
        self.assertTrue('Test subpage' in response.content.decode('utf-8'))


class AllArticlesTest(TestCase):

    def setUp(self):
        self.client = Client()
        testauthor = User.objects.create(username='testuser')
        for i in range(10):
            Article.objects.create(
                title='Article #%d' % i,
                content='<p>%d</p>' % i,
                published_date=(now() - timedelta(hours=i)),
                author=testauthor,
            )


    def test_get_all_articles(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
        for i in range(10):
            self.assertTrue('Article #%s' % i in response.content.decode('utf-8'))
            self.assertTrue('<p>%d</p>' % i in response.content.decode('utf-8'))


    def test_get_with_limits_json(self):
        last_article_on_frontpage = Article.objects.get(title='Article #5')
        before = last_article_on_frontpage.published_date.isoformat()
        response = self.client.get('/articles/',
            {'before': before, 'limit': 1},
            HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Article #6' in response.content.decode('utf-8'))
        self.assertTrue('<p>6</p>' in response.content.decode('utf-8'))
        self.assertFalse('Article #7' in response.content.decode('utf-8'))
