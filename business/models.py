from django.db import models
from django.forms import ValidationError

class Business(models.Model):
    user = models.ForeignKey('ml_auth.MusicLoversUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    logo = models.ImageField(upload_to='business-logos/')
    banner = models.ImageField(upload_to='business-banners/')
    address = models.CharField(max_length=100, blank=True)
    neighbourhood = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100)

    def average_rating(self):
        comments = BusinessComment.objects.filter(business=self)
        if comments.count() == 0:
            return 0
        else:
            sum = 0
            for comment in comments:
                sum += comment.rating
            return sum / comments.count()

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
        ('ELECTRO', 'Electro'),
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

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='events-banners/', blank=True)
    address = models.CharField(max_length=100, blank=True)
    neighbourhood = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    price = models.PositiveIntegerField()
    datetime = models.DateTimeField()
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=GENRES)




    def business_logo(self):
        return self.business.logo.url

    def __str__(self):
        return self.title


class EventPhoto(models.Model):
    event = models.ForeignKey('business.Event', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='events-images/')

    def __str__(self):
        return self.event.title


class EventComment(models.Model):
    event = models.ForeignKey('business.Event', on_delete=models.CASCADE)
    user = models.ForeignKey('ml_auth.MusicLoversUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def user_name(self):
        return self.user.username

    def user_logo(self):
        if self.user.logo:
            return self.user.logo.url
        else:
            return ''

    def event_name(self):
        return self.event.title

    def __str__(self):
        return self.event.title

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')
        super().save(*args, **kwargs)


class BusinessComment(models.Model):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)
    user = models.ForeignKey('ml_auth.MusicLoversUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def user_name(self):
        return self.user.username

    def user_logo(self):
        if self.user.logo:
            return self.user.logo.url
        else:
            return ''


    def __str__(self):
        return self.business.name

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')
        super().save(*args, **kwargs)
        
