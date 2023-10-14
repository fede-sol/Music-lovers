from django.db import models

class Business(models.Model):
    user = models.ForeignKey('ml_auth.MusicLoversUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='business-logos/')
    ciudad = models.CharField(max_length=100, blank=True)
    barrio = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusinessComment(models.Model):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    user = models.ForeignKey('ml_auth.MusicLoversUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.business.name


class BusinessPhoto(models.Model):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='business-images/')

    def __str__(self):
        return self.business.name




class Event(models.Model):
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

    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    barrio = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.PositiveIntegerField()
    datetime = models.DateTimeField()
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=GENRES)
    banner = models.ImageField(upload_to='events-banners/', blank=True)

    def __str__(self):
        return self.title


class EventPhoto(models.Model):
    event = models.ForeignKey('business.Event', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='business-logos/')

    def __str__(self):
        return self.event.title


class EventComment(models.Model):
    event = models.ForeignKey('business.Event', on_delete=models.CASCADE)
    user = models.ForeignKey('ml_auth.MusicLoversUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.event.title