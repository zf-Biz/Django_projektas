# Generated by Django 4.2.9 on 2024-01-21 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eparduotuve', '0004_profilis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilis',
            name='status',
            field=models.CharField(blank=True, choices=[('k', 'Kortele'), ('g', 'Grynaisiais'), ('p', 'Pavedimu'), ('d', 'Dovanų čekis')], default='k', help_text='Apmokėjimo būdo pasirinkimas', max_length=1, verbose_name='Apmokėjimas'),
        ),
    ]
