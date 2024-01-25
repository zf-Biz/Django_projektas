from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField
from datetime import date, time
import uuid

from PIL import Image


class Krepselis(models.Model):
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    PRISTATYMAS_STATUS = (
        ('p', _('Paštomatas')),
        ('k', _('Kurjeris')),
        ('a', _('Atsiėmimas parduotuvėje')),
    )
    pristatymas_status = models.CharField(max_length=1, choices=PRISTATYMAS_STATUS, blank=True,
                                          default='k', help_text=_('Krepšelio pristatymo pasirinkimas'),
                                          verbose_name=_('Būsena'))
    data = models.DateTimeField(_('Pristatymo data'), null=True, blank=True)
    PREKE_STATUS = (
        ('l', _('Laukiama apmokėjimo')),
        ('v', _('Vykdoma')),
        ('a', _('Atšaukta')),
    )
    status = models.CharField(max_length=1, choices=PREKE_STATUS, blank=True,
                              default='l', help_text=_('Krepšelio būsena'),
                              verbose_name=_('Būsena'))

    @property
    def is_overdue(self):
        if date.today().strftime("%Y-%m-%d %H:%M:%S") > str(self.data):
            return False
        else:
            return True

    @property
    def krepselio_suma(self):
        return sum([k_e.suma for k_e in self.krepselioeilutes_set.all()])

    def Uzsakyti(self):
        self.save()

    def krepselio_eilutes(self):
        return self.krepselioeilutes_set.all()

    def __str__(self):
        return f'{self.id} {self.data} {self.vartotojas}'

    class Meta:
        verbose_name = _('Krepšelis')
        verbose_name_plural = _('Krepšeliai')


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
        verbose_name = _('Krepšelio eilutė')
        verbose_name_plural = _('Krepšelio eilutės')


class Preke(models.Model):
    pavadinimas = models.CharField(_('Prekės pavadinimas'), max_length=200, blank=True)
    kategorija = models.ManyToManyField('Kategorija')
    vieneto_kaina = models.FloatField(_('Vieneto kaina'), null=True, blank=True)
    likutis = models.FloatField(_('Likutis'), null=True, blank=True)

    nuotrauka = models.ImageField(_('Nuotrauka'), upload_to='nuotraukos',
                                  null=True, blank=True)
    aprasymas = HTMLField(blank=True)

    def __str__(self):
        return f'{self.pavadinimas}'

    def prekes_kategorijos(self):
        return ', '.join(k.pavadinimas for k in self.kategorija.all())

    prekes_kategorijos.short_description = _('Kategorijos')

    class Meta:
        verbose_name = _('Prekė')
        verbose_name_plural = _('Prekės')


class Kategorija(models.Model):
    pavadinimas = models.CharField(_('Kategorijos pavadinimas'), max_length=100)

    def __str__(self):
        return f'{self.pavadinimas}'

    class Meta:
        verbose_name = _('Kategorija')
        verbose_name_plural = _('Kategorijos')


class Atsiliepimas(models.Model):
    preke = models.ForeignKey(Preke, on_delete=models.CASCADE, blank=True)
    vertintojas = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    turinys = models.TextField(_('Atsiliepimas'), max_length=2000)

    class Meta:
        verbose_name = _('Atsiliepimas')
        verbose_name_plural = _('Atsiliepimai')
        ordering = ['-data']


class PristatymoBudas(models.Model):
    atsiemimas = models.CharField(_('Atsiėmimo iš parduotuvės adresas'), max_length=100)
    pristatymas = models.CharField(_('Pristatymo adresas'), max_length=100)
    pastomatas = models.CharField(_('Paštomato adresas'), max_length=100)

    class Meta:
        verbose_name = _('Pristatymo būdas')
        verbose_name_plural = _('Pristatymo būdai')


class Profilis(models.Model):
    vartotojas = models.OneToOneField(User, on_delete=models.CASCADE)
    vardas = models.CharField(_('Vardas'), max_length=50)
    pavarde = models.CharField(_('Pavardė'), max_length=50)
    adresas = models.CharField(_('Adresas'), max_length=30, blank=True)
    u_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_('Unikalus vartotojo ID.'))
    kortele = models.CharField(max_length=13, verbose_name=_('Banko kortelės numeris'),
                               null=True, blank=True)
    APMOKEJIMO_BUDAS_STATUS = (
        ('k', _('Kortele')),
        ('g', _('Grynaisiais')),
        ('p', _('Pavedimu')),
        ('d', _('Dovanų čekis')),
    )
    status = models.CharField(max_length=1, choices=APMOKEJIMO_BUDAS_STATUS, blank=True,
                              default='k', help_text=_('Apmokėjimo būdo pasirinkimas'),
                              verbose_name=_('Apmokėjimas'))

    class Meta:
        verbose_name = _('Profilis')
        verbose_name_plural = _('Profiliai')

    def __str__(self):
        return f'{self.vartotojas}'
