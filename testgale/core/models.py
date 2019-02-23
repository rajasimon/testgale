from django.db import models


# Create your models here.
class Crawler(models.Model):
    url = models.URLField(unique=True)
    depth = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    link = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return "{}".format(self.url)


class Image(models.Model):
    url = models.URLField()
    crawlers = models.ManyToManyField(Crawler, blank=True)

    def __str__(self):
        return "{}".format(self.url)
