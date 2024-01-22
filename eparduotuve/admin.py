from django.contrib import admin

from .models import (Krepselis, KrepselioEilutes, Preke,
                     Kategorija, Atsiliepimas, PristatymoBudas, Profilis)


class KrepselioEilutesInLine(admin.TabularInline):
    model = KrepselioEilutes


class KrepselisAdmin(admin.ModelAdmin):
    list_display = ('pristatymo_budas', 'krepselio_suma',
                    'data', 'status')
    inlines = (KrepselioEilutesInLine,)


class KrepselioEilutesAdmin(admin.ModelAdmin):
    list_display = ('krepselis', 'preke', 'kiekis', 'suma')
    list_editable = ('preke', 'kiekis')


class PrekeAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'vieneto_kaina', 'likutis', 'prekes_kategorijos')
    list_editable = ('vieneto_kaina',)
    search_fields = ('pavadinimas', 'kategorija')


class KategorijaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas',)


class AtsiliepimasAdmin(admin.ModelAdmin):
    list_display = ('preke', 'data', 'vertintojas', 'turinys')


# class ProfilisAdmin(admin.ModelAdmin):
#     list_display = ('id', 'vartotojas', 'vardas', 'pavarde', 'kortele', 'status')
#     list_editable = ('vardas', 'pavarde', 'kortele', 'status')


class PristatymoBudasAdmin(admin.ModelAdmin):
    list_display = ('atsiemimas', 'pristatymas', 'pastomatas')


admin.site.register(Krepselis, KrepselisAdmin)
admin.site.register(KrepselioEilutes, KrepselioEilutesAdmin)
admin.site.register(Preke, PrekeAdmin)
admin.site.register(Kategorija, KategorijaAdmin)
admin.site.register(Profilis)  # , ProfilisAdmin
admin.site.register(Atsiliepimas, AtsiliepimasAdmin)
admin.site.register(PristatymoBudas, PristatymoBudasAdmin)
