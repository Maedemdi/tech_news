from rest_framework.test import APITestCase
from django.urls import reverse

from .models import NewsItem, Tag, Source

class NewsItemAPITestCase(APITestCase):
    """ Testing functionalities """

    def setUp(self):
        # Creating objects
        tag1 = Tag.objects.create(caption = 'Politics')
        tag2 = Tag.objects.create(caption = 'Hot')
        source1 = Source.objects.create(name = 'Source1', url = 'source1.url.org')
        source2 = Source.objects.create(name = 'Source2', url = 'source2.url.org')
        news1 = NewsItem.objects.create(title = 'The First Item', text = 'The First Item Text')
        news1.tags.add(tag1)
        news1.source.add(source1)
        news2 = NewsItem.objects.create(title = 'The Second Item', text = 'The Second Item Text')
        news2.tags.add(tag1, tag2)
        news2.source.add(source2)
        news3 = NewsItem.objects.create(title = 'The Third Item', text = 'The Third Item Text')
        news3.tags.add(tag2)
        news3.source.add(source1, source2)
        print(NewsItem.objects.all())

    def test_list_news(self):
        # Test if all the news are listed
        url = reverse('news-url-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_tag(self):
        # Test if news with tag "Politics" are displayed correctly
        url = reverse('news-url-list') + '?tags=Politics'
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        for news in response.data:
            self.assertIn('Politics', [tag['caption'] for tag in news['tags']])

    def test_search_include_only(self):
        # Test if we can seach the news by including a certain word
        url = reverse('news-url-list') + '?search=second'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        titles = [news['title'] for news in response.data]
        self.assertNotIn("The First Item", titles)
        self.assertIn("The Second Item", titles)
        self.assertNotIn("The Third Item", titles)

    def test_search_exclude_only(self):
        # Test if we can seach the news by excluding a certain word
        url = reverse('news-url-list') + '?search=-second'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        titles = [news['title'] for news in response.data]
        self.assertIn("The First Item", titles)
        self.assertNotIn("The Second Item", titles)
        self.assertIn("The Third Item", titles)

    def test_search_include_and_exclude(self):
        # Test if we can search by both including and excluding words
        url = reverse('news-url-list') + '?search=-second first'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        titles = [news['title'] for news in response.data]
        self.assertIn("The First Item", titles)
        self.assertNotIn("The Second Item", titles)
        self.assertNotIn("The Third Item", titles)
        