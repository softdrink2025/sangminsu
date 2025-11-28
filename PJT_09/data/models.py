from django.db import models

# Create your models here.
# genreId는 나중에 필드명 변경 必
class Track(models.Model):
    genreId= models.ManyToManyField('Genre', blank=True)
    track_name = models.TextField()
    track_id = models.TextField()
    track_popularity = models.IntegerField()
    artist_name = models.TextField()
    artist_id = models.TextField()
    release_year = models.DateField()
    duration_ms = models.IntegerField()
    track_image_link = models.URLField()

    def set_default_genre(self):
        # Track이 생성될 때 기본 장르를 할당
        default_genre = Genre.objects.get(name="Undefined")  # Undefined를 기본으로
        self.genreId.add(default_genre)

class Genre(models.Model):
    genre = models.TextField()