from django.db import models



class UserPreferences(models.Model):

    GENRES = (
        ('ROCK', 'Rock'),
        ('POP', 'Pop'),
        ('ELECTRONICA', 'Electronica'),
        ('HIPHOP', 'Hip Hop'),
        ('REGGAE', 'Reggae'),
        ('REGGAETON', 'Reggaeton'),
        ('CUMBIA', 'Cumbia'),
        ('SALSA', 'Salsa'),
        ('TANGO', 'Tango'),
        ('FOLKLORE', 'Folklore'),
        ('JAZZ', 'Jazz'),
        ('BLUES', 'Blues'),
        ('OTRO', 'Otro'),
    )

    user = models.ForeignKey('ml_auth.MusicLoversUser', on_delete=models.CASCADE)
    genre1 = models.CharField(max_length=50, choices=GENRES,blank=True, null=True)
    genre2 = models.CharField(max_length=50, choices=GENRES,blank=True, null=True)
    genre3 = models.CharField(max_length=50, choices=GENRES,blank=True, null=True)

    def __str__(self):
        return self.user.username
