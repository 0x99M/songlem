import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from core.models import Artist, Album, Song, AlbumArtist, SongArtist

# Default number of items to create
DEFAULT_ARTISTS = 5
DEFAULT_ALBUMS = 10
DEFAULT_SONGS_PER_ALBUM = 3


class Command(BaseCommand):
    """
    A Django management command to seed the database with fake data.
    Example usage:
    python manage.py seed
    python manage.py seed --artists 20 --albums 50 --songs-per-album 15
    """

    help = "Seeds the database with fake data for artists, albums, and songs."

    def add_arguments(self, parser):
        parser.add_argument(
            "--artists",
            type=int,
            help=f"The number of artists to create. Defaults to {DEFAULT_ARTISTS}.",
            default=DEFAULT_ARTISTS,
        )
        parser.add_argument(
            "--albums",
            type=int,
            help=f"The number of albums to create. Defaults to {DEFAULT_ALBUMS}.",
            default=DEFAULT_ALBUMS,
        )
        parser.add_argument(
            "--songs-per-album",
            type=int,
            help=f"The average number of songs to create per album. Defaults to {DEFAULT_SONGS_PER_ALBUM}.",
            default=DEFAULT_SONGS_PER_ALBUM,
        )
        parser.add_argument(
            "--no-clean",
            action="store_true",
            help="Do not delete existing data before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding the database...")

        num_artists = options["artists"]
        num_albums = options["albums"]
        num_songs_per_album = options["songs_per_album"]
        clean_data = not options["no_clean"]

        if num_artists == 0 or num_albums == 0:
            self.stdout.write(
                self.style.WARNING("Cannot seed data with 0 artists or albums. Aborting.")
            )
            return

        fake = Faker()

        if clean_data:
            self.stdout.write("Deleting existing data...")
            # Order of deletion matters. Or rely on on_delete=CASCADE.
            Song.objects.all().delete()
            Album.objects.all().delete()
            Artist.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Successfully deleted existing data."))

        # 1. Bulk create Artists
        self.stdout.write(f"Generating {num_artists} artists...")
        artists_to_create = [
            Artist(first_name=fake.first_name(), last_name=fake.last_name())
            for _ in range(num_artists)
        ]
        artists = Artist.objects.bulk_create(artists_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_artists} artists."))

        # 2. Bulk create Albums
        self.stdout.write(f"Generating {num_albums} albums...")
        albums_to_create = [
            Album(
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=500),
                date_created=fake.date_this_decade(),
            )
            for _ in range(num_albums)
        ]
        albums = Album.objects.bulk_create(albums_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_albums} albums."))

        # 3. Prepare Songs and relationship objects in memory
        self.stdout.write("Generating songs and relationships...")
        songs_to_create = []
        album_artists_to_create = []
        song_artists_to_create = []

        for album in albums:
            # Album-Artist links
            album_artist_sample = random.sample(artists, k=random.randint(1, min(3, num_artists)))
            for artist in album_artist_sample:
                album_artists_to_create.append(AlbumArtist(album=album, artist=artist))

            # Song objects for this album
            for _ in range(random.randint(max(1, num_songs_per_album - 4), num_songs_per_album + 4)):
                songs_to_create.append(
                    Song(title=fake.sentence(nb_words=random.randint(2, 5)).replace(".", ""),
                         description=fake.text(max_nb_chars=200),
                         date=fake.date_between(start_date=album.date_created),
                         link=fake.url(),
                         album=album)
                )

        # 4. Bulk create Songs, then create their M2M links
        self.stdout.write(f"Creating {len(songs_to_create)} songs in the database...")
        songs = Song.objects.bulk_create(songs_to_create)

        for song in songs:
            song_artist_sample = random.sample(artists, k=random.randint(1, min(2, num_artists)))
            for artist in song_artist_sample:
                song_artists_to_create.append(SongArtist(song=song, artist=artist))

        self.stdout.write("Creating all relationships...")
        AlbumArtist.objects.bulk_create(album_artists_to_create)
        SongArtist.objects.bulk_create(song_artists_to_create)

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))