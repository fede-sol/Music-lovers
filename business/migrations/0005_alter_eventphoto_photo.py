# Generated by Django 4.2.5 on 2023-10-18 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_event_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventphoto',
            name='photo',
            field=models.ImageField(upload_to='events-images/'),
        ),
    ]
