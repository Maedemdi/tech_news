from django.test import TestCase

from ..models import News, Tag
from ..filters import NewsFilter


class NewsFilterTests(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(label='django')
        self.news1 = News.objects.create(
            title='Django tutorial',
            content='something about django',
            author='me',
            date='2026-01-01',
            url='https://example.com/1',
        )
        self.news2 = News.objects.create(
            title='Python tutorial',
            content='something about python ig',
            author='me',
            date='2026-01-02',
            url='https://example.com/2',
        )
        self.news3 = News.objects.create(
            title='DRF tutorial',
            content='something about django rest framewrok',
            author='me',
            date='2026-01-03',
            url='https://example.com/3',
        )

    def test_included_word_filter(self):
        filter_data = {'included_word': 'django'}
        news_filter = NewsFilter(
            data=filter_data,
            queryset=News.objects.all()
        )
        self.assertTrue(news_filter.is_valid())
        results = news_filter.qs
        self.assertEqual(results.count(), 2)
        self.assertIn(self.news1, results)
        self.assertIn(self.news3, results)

    def test_excluded_word_filter(self):
        filter_data = {'excluded_word': 'django'}
        news_filter = NewsFilter(
            data=filter_data,
            queryset=News.objects.all()
        )
        self.assertTrue(news_filter.is_valid())
        results = news_filter.qs
        self.assertEqual(results.count(), 1)
        self.assertIn(self.news2, results)
        self.assertNotIn(self.news1, results)
        self.assertNotIn(self.news3, results)

    def test_included_word_filter_is_case_insensitive(self):
        filter_data = {'included_word': 'DJANGO'}
        news_filter = NewsFilter(
            data=filter_data,
            queryset=News.objects.all()
        )
        self.assertTrue(news_filter.is_valid())
        self.assertEqual(news_filter.qs.count(), 2)