from django.db import models

from django.db import models
# from django.contrib.auth.models import User
# from django.utils.translation import gettext_lazy as _

# from tinymce.models import HTMLField
from datetime import date
import uuid


# from PIL import Image


class Krepselis(models.Model):
    # profilio_unikalus_id = models.ForeignKey('Profilis', on_delete=models.SET_NULL,
    #                                          null=True, related_name='uuid')
    pristatymo_budas = models.ForeignKey('Pristatymobudas', on_delete=models.SET_NULL,
                                         null=True, related_name='budas')
    data = models.DateTimeField('Pristatymo data', null=True, blank=True)
    PREKE_STATUS = (
        ('l', 'Laukiama apmokėjimo'),
        ('v', 'Vykdoma'),
        ('a', 'Atšaukta'),
    )
    status = models.CharField(max_length=1, choices=PREKE_STATUS, blank=True,
                              default='l', help_text='Krepšelio būsena',
                              verbose_name='Būsena')

    @property
    def krepselio_suma(self):
        return sum([k_e.suma for k_e in self.krepselioeilutes_set.all()])

    class Meta:
        verbose_name = 'Krepšelis'
        verbose_name_plural = 'Krepšeliai'


class KrepselioEilutes(models.Model):
    krepselis = models.ForeignKey(Krepselis, on_delete=models.SET_NULL,
                                  null=True, verbose_name='Krepšelio numeris')
    preke = models.ForeignKey('Preke', on_delete=models.SET_NULL,
                              null=True, verbose_name='Prekė')
    kiekis = models.IntegerField('Kiekis', null=True, blank=True)

    @property
    def suma(self):
        return self.preke.vieneto_kaina * self.kiekis

    class Meta:
        verbose_name = 'Krepšelio eilutė'
        verbose_name_plural = 'Krepšelio eilutės'


class Preke(models.Model):
    pavadinimas = models.CharField('Prekės pavadinimas', max_length=200, blank=True)
    kategorija = models.ManyToManyField('Kategorija')
    vieneto_kaina = models.FloatField('Vieneto kaina', null=True, blank=True)
    likutis = models.FloatField('Likutis', null=True, blank=True)
    # nuotrauka = models.ImageField('Nuotrauka', upload_to='nuotraukos',
    #                               null=True, blank=True)

    def __str__(self):
        return f'{self.pavadinimas}'

    def prekes_kategorijos(self):
        return ', '.join(k.pavadinimas for k in self.kategorija.all())

    prekes_kategorijos.short_description = 'Kategorijos'

    class Meta:
        verbose_name = 'Prekė'
        verbose_name_plural = 'Prekės'


class Kategorija(models.Model):
    pavadinimas = models.CharField('Kategorijos pavadinimas', max_length=100)

    def __str__(self):
        return f'{self.pavadinimas}'

    class Meta:
        verbose_name = 'Kategorija'
        verbose_name_plural = 'Kategorijos'


class Atsiliepimas(models.Model):
    preke = models.ForeignKey(Preke, on_delete=models.CASCADE, blank=True)
    # vertintojas = models.ForeignKey(User, on_delete=models.SET_NULL,
    #                                 blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    turinys = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = 'Atsiliepimas'
        verbose_name_plural = 'Atsiliepimai'


class PristatymoBudas(models.Model):
    atsiemimas = models.CharField('Atsiėmimo iš parduotuvės adresas', max_length=100)
    pristatymas = models.CharField('Pristatymo adresas', max_length=100)
    pastomatas = models.CharField('Paštomato adresas', max_length=100)

    class Meta:
        verbose_name = 'Pristatymo būdas'
        verbose_name_plural = 'Pristatymo būdai'
