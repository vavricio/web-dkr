from django.db import models
from django.conf import settings
from redis import Redis

redis = Redis(settings.REDIS_HOST, port=int(settings.REDIS_PORT))


class AnimeWatching(models.Model):
    WATCHING = [
        ('Finished', 'Finished'),
        ('In process', 'In process'),
        ('Dropped', 'Dropped'),
        ('Plans to watch', 'Plans to watch'),
    ]

    RATING = [
        ('11/10', '11/10'),
        ('10/10', '10/10'),
        ('9/10', '9/10'),
        ('8/10', '8/10'),
        ('7/10', '7/10'),
        ('6/10', '6/10'),
        ('5/10', '5/10'),
        ('4/10', '4/10'),
        ('3/10', '3/10'),
        ('2/10', '2/10'),
        ('1/10', '1/10'),
        ('0/10', '0/10'),
    ]

    anime_name = models.CharField(max_length=100)
    rating = models.CharField(max_length=5, choices=RATING)
    watching = models.CharField(max_length=50, choices=WATCHING)

    def as_dict(self):
        return {
            'anime_name': self.anime_name,
            'rating': self.rating,
            'watching': self.watching,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
