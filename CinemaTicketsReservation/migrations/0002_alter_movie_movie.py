# Generated by Django 4.0.3 on 2022-07-26 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CinemaTicketsReservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie',
            field=models.CharField(max_length=50),
        ),
    ]
