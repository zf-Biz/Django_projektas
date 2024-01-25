# Generated by Django 4.2.9 on 2024-01-25 09:26

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('eparduotuve', '0013_krepselioeilutes_vartotojas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='krepselioeilutes',
            name='vartotojas',
        ),
        migrations.AddField(
            model_name='preke',
            name='aprasymas',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]
