from django.db import models


class Tag(models.Model):
    label = models.CharField()

    def __str__(self):
        return self.label

class News(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    url = models.URLField()
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title
    
