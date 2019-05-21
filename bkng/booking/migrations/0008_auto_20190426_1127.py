# Generated by Django 2.2 on 2019-04-26 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_booking_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='service',
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.ManyToManyField(related_name='servtype', to='booking.ServiceType'),
        ),
    ]
