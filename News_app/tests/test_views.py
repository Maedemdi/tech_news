from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ..views import NewsViewset, TagViewset
from ..models import News, Tag


class TagViewset_Test(APITestCase):

    def test_tags_list_status_code(self):
        response = self.client.get(reverse('tags-list'))
        self.assertEqual(response.status_code, 200)

    def test_correct_tags_post_request(self):
        url = reverse('tags-list')
        dummy_data = {'label': 'something'}
        response = self.client.post(url, dummy_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().label, 'something')


class NewsViewset_Test(APITestCase):

    def test_news_list_status_code(self):
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, 200)

    def test_correct_news_post_request(self):
        Tag.objects.create(label='idk')
        url = reverse('news-list')
        dummy_data = {
            'title': 'testing',
            'content': 'testing',
            'date': '2026-01-01',
            'author': 'maede',
            'url': 'https://something.com/',
            'tags': ['idk']}
        response = self.client.post(url, dummy_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.get().title, 'testing')
