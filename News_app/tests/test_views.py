from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ..views import NewsViewset, TagViewset
from ..models import News, Tag


class NewsViewSet_Test(APITestCase):

    def test_home_status_code(self):
        response = self.client.get('/')
        # reverse('news_list')
        self.assertEqual(response.status_code, 200)

    def test_post_status_code(self):
        some_tag = Tag.objects.create(label='idk')
        url = '/'
        dummy_data = {
            'title':'testing',
            'content': 'testing',
            'date' : '0101-01-01',
            'author': 'maede',
            'url':'https://127.0.0.1',}
            # 'tags': [some_tag]}
        response = self.client.post(url, dummy_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.get().title, 'testing')

