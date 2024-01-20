from django.contrib import admin

from .models import (Krepselis, KrepselioEilutes, Preke,
                      Kategorija, Atsiliepimas, PristatymoBudas)


class KrepselioEilutesInLine(admin.TabularInline):
    model = KrepselioEilutes


class KrepselisAdmin(admin.ModelAdmin):
    list_display = ('profilio_unikalus_id', 'pristatymo_budas', 'krepselio_suma',
                    'data', 'status')
    inlines = (KrepselioEilutesInLine,)


class KrepselioEilutesAdmin(admin.ModelAdmin):
    list_display = ('krepselis', 'preke', 'kiekis', 'suma')
    list_editable = ('preke', 'kiekis')


class PrekeAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'vieneto_kaina', 'likutis', 'prekes_kategorijos')
    list_editable = ('vieneto_kaina',)


class KategorijaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas',)


# class ProfilisAdmin(admin.ModelAdmin):
#     list_display = ('id', 'vartotojas', 'vardas', 'pavarde', 'kortele', 'status')
#     list_editable = ('vardas', 'pavarde', 'kortele', 'status')


class PristatymoBudasAdmin(admin.ModelAdmin):
    list_display = ('atsiemimas', 'pristatymas', 'pastomatas')


admin.site.register(Krepselis)
admin.site.register(KrepselioEilutes, )
admin.site.register(Preke)
admin.site.register(Kategorija)
# admin.site.register(Profilis, ProfilisAdmin)
admin.site.register(Atsiliepimas)
admin.site.register(PristatymoBudas)
