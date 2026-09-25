<<<<<<< HEAD
from django.db import models
=======
from django.db import models


class Tag(models.Model):
    label = models.CharField()

    def __str__(self):
        return self.label

class News(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title
    
>>>>>>> Challenge-1
