from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from django.contrib.auth.decorators import login_required

from .models import (Krepselis, KrepselioEilutes, Preke,
                     Kategorija, Atsiliepimas, PristatymoBudas)


# @login_required
def index(request):
    return render(request, 'index.html')


class KategorijaListView(generic.ListView):
    model = Kategorija
    context_object_name = "kategorija_list"
    template_name = 'kategorija_list.html'


class KategorijaDetailView(generic.DetailView):  # generic.edit.FormMixin,
    model = Kategorija
    context_object_name = "kategorija"
    template_name = "kategorija_detail.html"


class PrekesListView(generic.ListView):  # LoginRequiredMixin,
    model = Preke
    context_object_name = "preke_list"
    template_name = "preke_list.html"
    paginate_by = 4


class PrekeDetailView(generic.DetailView):  # generic.edit.FormMixin,
    model = Preke
    context_object_name = "preke"
    template_name = "preke_detail.html"
