# pictures/models.py
# Description: This file contains the model for the PhotoGallery class

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


class PhotoGallery(models.Model):
    media = models.CharField(max_length=100, blank=False)
    sectionTitle = models.CharField(max_length= 200, blank=False)
    pubDate = models.DateTimeField()
    pageUrl = models.URLField(null=False, blank=False)
    caption = models.TextField()
    location = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length= 50, blank=True)
    credits = models.CharField(max_length= 50, blank=True)
    picture = models.URLField(null=False, blank=False)
    pictureEditor = models.CharField(max_length=100, blank=True, null=True)
    ratings = GenericRelation(Rating, related_query_name='photo_galleries')

    class Meta:
        unique_together = ['caption', 'picture']
        ordering= ['-pubDate']
        verbose_name = 'Picture'

    def __str__(self):
        return f'{self.media}'
