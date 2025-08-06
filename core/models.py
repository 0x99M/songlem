import uuid
from django.db import models

class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_created = models.DateField()

    artists = models.ManyToManyField(Artist, through='AlbumArtist', related_name='albums')

    def __str__(self):
        return self.title

class AlbumArtist(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('album', 'artist')

class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    link = models.URLField()

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    artists = models.ManyToManyField(Artist, through='SongArtist', related_name='songs')

    def __str__(self):
        return self.title

class SongArtist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('song', 'artist')