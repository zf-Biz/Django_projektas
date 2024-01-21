# Generated by Django 4.2.9 on 2024-01-21 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eparduotuve', '0002_preke_nuotrauka'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='atsiliepimas',
            options={'ordering': ['-data'], 'verbose_name': 'Atsiliepimas', 'verbose_name_plural': 'Atsiliepimai'},
        ),
        migrations.AddField(
            model_name='atsiliepimas',
            name='vertintojas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
