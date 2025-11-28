from django.db import models

# Create your models here.
class Track(models.Model):
    track_name = models.TextField()
    track_id = models.TextField()
    track_popularity = models.IntegerField()
    artist_name = models.TextField()
    artist_id = models.TextField()
    release_year = models.DateField()
    duration_ms = models.IntegerField()
    track_image_link = models.URLField()