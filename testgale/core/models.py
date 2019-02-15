from django.db import models


# Create your models here.
class Crawler(models.Model):
    url = models.URLField()
    depth = models.IntegerField()
    is_completed = models.BooleanField(default=False)


class Link(models.Model):
    url = models.URLField()
    crawlers = models.ManyToManyField(Crawler, blank=True)


class Image(models.Model):
    url = models.URLField()
    crawlers = models.ManyToManyField(Crawler, blank=True)
