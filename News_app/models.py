from django.db import models

class NewsItem(models.Model):
    """ Every Item of the news """
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateField(auto_now_add= True)
    updated_at = models.DateField(auto_now= True)
    tags = models.ManyToManyField("Tag")
    source = models.OneToOneField("Source", on_delete= models.CASCADE, null= True)



class Tag(models.Model):
    """ Enables tagging each news item """
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption
    


class Source(models.Model):
    """ Sources of each news item """
    name = models.CharField(max_length=100, null= True)
    url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    