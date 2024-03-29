# Generated by Django 4.2.9 on 2024-01-20 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategorija',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(max_length=100, verbose_name='Kategorijos pavadinimas')),
            ],
            options={
                'verbose_name': 'Kategorija',
                'verbose_name_plural': 'Kategorijos',
            },
        ),
        migrations.CreateModel(
            name='PristatymoBudas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atsiemimas', models.CharField(max_length=100, verbose_name='Atsiėmimo iš parduotuvės adresas')),
                ('pristatymas', models.CharField(max_length=100, verbose_name='Pristatymo adresas')),
                ('pastomatas', models.CharField(max_length=100, verbose_name='Paštomato adresas')),
            ],
            options={
                'verbose_name': 'Pristatymo būdas',
                'verbose_name_plural': 'Pristatymo būdai',
            },
        ),
        migrations.CreateModel(
            name='Preke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(blank=True, max_length=200, verbose_name='Prekės pavadinimas')),
                ('vieneto_kaina', models.FloatField(blank=True, null=True, verbose_name='Vieneto kaina')),
                ('likutis', models.FloatField(blank=True, null=True, verbose_name='Likutis')),
                ('kategorija', models.ManyToManyField(to='eparduotuve.kategorija')),
            ],
            options={
                'verbose_name': 'Prekė',
                'verbose_name_plural': 'Prekės',
            },
        ),
        migrations.CreateModel(
            name='Krepselis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(blank=True, null=True, verbose_name='Pristatymo data')),
                ('status', models.CharField(blank=True, choices=[('l', 'Laukiama apmokėjimo'), ('v', 'Vykdoma'), ('a', 'Atšaukta')], default='l', help_text='Krepšelio būsena', max_length=1, verbose_name='Būsena')),
                ('pristatymo_budas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='budas', to='eparduotuve.pristatymobudas')),
            ],
            options={
                'verbose_name': 'Krepšelis',
                'verbose_name_plural': 'Krepšeliai',
            },
        ),
        migrations.CreateModel(
            name='KrepselioEilutes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kiekis', models.IntegerField(blank=True, null=True, verbose_name='Kiekis')),
                ('krepselis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eparduotuve.krepselis', verbose_name='Krepšelio numeris')),
                ('preke', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eparduotuve.preke', verbose_name='Prekė')),
            ],
            options={
                'verbose_name': 'Krepšelio eilutė',
                'verbose_name_plural': 'Krepšelio eilutės',
            },
        ),
        migrations.CreateModel(
            name='Atsiliepimas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('turinys', models.TextField(max_length=2000, verbose_name='Atsiliepimas')),
                ('preke', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='eparduotuve.preke')),
            ],
            options={
                'verbose_name': 'Atsiliepimas',
                'verbose_name_plural': 'Atsiliepimai',
            },
        ),
    ]
