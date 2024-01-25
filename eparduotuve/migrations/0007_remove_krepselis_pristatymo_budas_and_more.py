# Generated by Django 4.2.9 on 2024-01-22 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eparduotuve', '0006_profilis_adresas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='krepselis',
            name='pristatymo_budas',
        ),
        migrations.AddField(
            model_name='krepselis',
            name='pristatymas_status',
            field=models.CharField(blank=True, choices=[('p', 'Paštomatas'), ('k', 'Kurjeris'), ('a', 'Atsiėmimas parduotuvėje')], default='k', help_text='Krepšelio pristatymo pasirinkimas', max_length=1, verbose_name='Būsena'),
        ),
        migrations.AddField(
            model_name='krepselis',
            name='profilio_unikalus_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uuid', to='eparduotuve.profilis'),
        ),
    ]
