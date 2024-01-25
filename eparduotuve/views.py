from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin

from django.contrib.auth.decorators import login_required

from .models import (Krepselis, KrepselioEilutes, Preke,
                     Kategorija, Atsiliepimas, PristatymoBudas)
from .forms import (PrekeAtsiliepimasForm, UserUpdateForm,
                    ProfileUpdateForm, UserKrepselisCreateForm, UserKrepselioEilutesCreateForm)


@login_required
def index(request):
    return render(request, 'index.html')


class KategorijaListView(LoginRequiredMixin, generic.ListView):
    model = Kategorija
    context_object_name = "kategorija_list"
    template_name = 'kategorija_list.html'


class KategorijaDetailView(LoginRequiredMixin, generic.DetailView):  # generic.edit.FormMixin,
    model = Kategorija
    context_object_name = "kategorija"
    template_name = "kategorija_detail.html"


class PrekesListView(LoginRequiredMixin, generic.ListView):  # LoginRequiredMixin,
    model = Preke
    context_object_name = "preke_list"
    template_name = "preke_list.html"
    paginate_by = 6


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


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)


class VartotojoKrepselisListView(LoginRequiredMixin, generic.ListView):
    model = Krepselis
    template_name = 'krepseliai.html'
    context_object_name = 'krepselis'

    def get_queryset(self):
        return Krepselis.objects.filter(vartotojas=self.request.user.id).order_by('data')


class VartotojoKrepselisDetailView(LoginRequiredMixin, generic.DetailView):  # generic.edit.FormMixin,
    model = Krepselis
    context_object_name = "krepselis"
    template_name = "krepselis.html"


class KrepselisByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Krepselis
    success_url = '/eparduotuve/krepseliai/'
    template_name = 'naujas_krepselis.html'
    form_class = UserKrepselisCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)


class KrepselisByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Krepselis
    template_name = 'krepselis_update.html'
    form_class = UserKrepselisCreateForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("mano-krepselis", kwargs={"pk": pk})

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        krepselis_o = self.get_object()
        return krepselis_o.vartotojas == self.request.user


class KrepselisByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Krepselis
    success_url = '/eparduotuve/krepseliai/'
    template_name = 'krepselis_delete.html'

    def test_func(self):
        krepselis_o = self.get_object()
        return krepselis_o.vartotojas == self.request.user


class KrepselioEiluteByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = KrepselioEilutes
    # success_url =
    template_name = 'krepselio_eilutes_update.html'
    form_class = UserKrepselioEilutesCreateForm

    # fields = ('book','due_back') #alternatyva greitam testavimui

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        krepseliseilutes_o = self.get_object()
        return krepseliseilutes_o.krepselis.vartotojas == self.request.user

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("mano-krepselis", kwargs={"pk": pk})


class KrepselioEiluteByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = KrepselioEilutes
    template_name = 'krepselio_eilutes_update.html'
    form_class = UserKrepselioEilutesCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("mano-krepselis", kwargs={"pk": pk})


class KrepselioEiluteByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = KrepselioEilutes
    success_url = '/eparduotuve/krepseliai/'
    template_name = 'krepselio_eilutes_delete.html'

    def test_func(self):
        krepselioeilute_o = self.get_object()
        return krepselioeilute_o.krepselis.vartotojas == self.request.user

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("mano-krepselis", kwargs={"pk": pk})

# @login_required
# def prideti_preke(request):
#     if request.method == "POST":
#         krepselis_form = KrepselisByUserUpdateView(request.POST)
#         krepselioeilutes_form = KrepselioEiluteByUserUpdateView(request.POST, request.FILES)
#         if krepselis_form.is_valid() and krepselioeilutes_form.is_valid():
#             krepselis_form.save()
#             krepselioeilutes_form.save()
#             messages.success(request, f"Prekė pridėta")
#             return redirect('prekes')
#     else:
#         krepselis_form = KrepselisByUserUpdateView(instance=request.user)
#         krepselioeilutes_form = KrepselioEiluteByUserUpdateView(instance=request.user.profilis)
#
#     context = {
#         'krepselis_form': krepselis_form,
#         'krepselioeilutes_form': krepselioeilutes_form,
#     }
#     return render(request, 'krepselis_update.html', context)
