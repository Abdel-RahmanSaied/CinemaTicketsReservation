# Generated by Django 4.0.3 on 2022-07-26 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CinemaTicketsReservation', '0002_alter_movie_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='date',
        ),
    ]
