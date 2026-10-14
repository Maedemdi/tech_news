from django.test import TestCase

from ..serializers import NewsSerializer, TagSerializer
from .. import models

# Tag serializer does not have to be tested since it does not contain any custom logic


class NewsSerializer_Test(TestCase):

    def setUp(self):
        self.tag = models.Tag.objects.create(label='testing_tag')
        self.valid_data = {
            'title': 'testing',
            'content': 'some content regarding testing',
            'author': 'me',
            'date': '2026-01-01',
            'url': 'https://something.org',
            'tags': ['testing_tag'],
        }

    def test_valid_data(self):
        serializer = NewsSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data['title'],
            'testing'
        )

    def test_tags_are_converted_to_tag_objects(self):
        serializer = NewsSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data['tags'],
            [self.tag]
        )

    def test_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''
        serializer = NewsSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_serialized_data_contains_tag_labels(self):
        news = models.News.objects.create(
            title='testing',
            content='some content regarding testing',
            author='me',
            date='2026-01-01',
            url='https://something.org',
        )
        news.tags.add(self.tag)
        serializer = NewsSerializer(news)
        self.assertEqual(serializer.data['tags'], ['testing_tag'])
