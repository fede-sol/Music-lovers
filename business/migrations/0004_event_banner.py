# Generated by Django 4.2.5 on 2023-10-14 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_alter_businessphoto_photo_alter_eventphoto_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='banner',
            field=models.ImageField(blank=True, upload_to='events-banners/'),
        ),
    ]