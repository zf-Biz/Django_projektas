from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Atsiliepimas, User, Preke, Profilis, Krepselis, KrepselioEilutes


class PrekeAtsiliepimasForm(forms.ModelForm):
    class Meta:
        model = Atsiliepimas
        fields = ('turinys', 'preke', 'vertintojas')
        widgets = {  # paslepiam laukus, kad būtų nevaizduojami formoje
            'preke': forms.HiddenInput(),
            'vertintojas': forms.HiddenInput(),

        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ('vardas', 'pavarde', 'kortele', 'status')


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


class UserKrepselisCreateForm(forms.ModelForm):
    class Meta:
        model = Krepselis
        fields = ('vartotojas', 'data', 'pristatymas_status', 'status')
        widgets = {
            'vartotojas': forms.HiddenInput(),
            'data': DateInput(),
        }


class UserKrepselioEilutesCreateForm(forms.ModelForm):
    class Meta:
        model = KrepselioEilutes
        fields = ('krepselis', 'preke', 'kiekis')
        # widgets = {
        #     'krepselis': forms.HiddenInput(),
        # }


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
