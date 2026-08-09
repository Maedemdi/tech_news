from django.test import TestCase
from ..models import News, Tag


class TagModelTest(TestCase):

    def test_str(self):
        self.tag = Tag(label='some_tag')
        self.assertEqual(str(self.tag), 'some_tag')


class NewsModelTest(TestCase):

    def test_str(self):
        some_tag = Tag.objects.create(label='idk')
        another_tag = Tag.objects.create(label='another_idk')
        self.news = News.objects.create(title='some_title', content='some_content',
                                        date='0202-02-02', author='me', url='https://127.0.0.1',)
        self.news.tags.set([some_tag, another_tag])
        self.assertEqual(str(self.news), 'some_title')
