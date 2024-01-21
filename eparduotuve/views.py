from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin

from django.contrib.auth.decorators import login_required

from .models import (Krepselis, KrepselioEilutes, Preke,
                     Kategorija, Atsiliepimas, PristatymoBudas)
from .forms import PrekeAtsiliepimasForm


@login_required
def index(request):
    return render(request, 'index.html')


class KategorijaListView(LoginRequiredMixin, generic.ListView):
    model = Kategorija
    context_object_name = "kategorija_list"
    template_name = 'kategorija_list.html'


class KategorijaDetailView(generic.DetailView):  # generic.edit.FormMixin,
    model = Kategorija
    context_object_name = "kategorija"
    template_name = "kategorija_detail.html"


class PrekesListView(LoginRequiredMixin, generic.ListView):  # LoginRequiredMixin,
    model = Preke
    context_object_name = "preke_list"
    template_name = "preke_list.html"
    paginate_by = 4


class PrekeDetailView(LoginRequiredMixin, generic.DetailView, FormMixin):  # generic.edit.FormMixin,
    model = Preke
    context_object_name = "preke"
    template_name = "preke_detail.html"
    form_class = PrekeAtsiliepimasForm

    def get_success_url(self):
        return reverse('preke', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.preke = self.object
        form.instance.vertintojas = self.request.user
        form.save()
        return super(PrekeAtsiliepimasForm, self).form_valid(form)


def search(request):
    query = request.GET["search_text"]
    preke_results = Preke.objects.filter(Q(pavadinimas__icontains=query))
    kategorija_results = Kategorija.objects.filter(Q(pavadinimas__icontains=query))

    return render(request, "search.html", context={"preke_objects": preke_results,
                                                   "kategorija_objects": kategorija_results,
                                                   "query": query})


@csrf_protect
def register_user(request):
    if request.method != "POST":
        return render(request, 'registration/registration.html')

    # jeigu POST
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    password2 = request.POST["password2"]

    if password != password2:
        messages.error(request, ("Passwords don't match!!!"))

    if User.objects.filter(username=username).exists():
        messages.error(request, ("User %s already exists!!!") % username)

    if User.objects.filter(email=email).exists():
        messages.error(request, (f"Email {email} already registered!!!"))

    if messages.get_messages(request):
        return redirect('register')

    User.objects.create_user(username=username, email=email, password=password)
    messages.success(request, ("User %s created!!!") % username)
    return redirect('index')
