from django import forms

from .models import Atsiliepimas, User, Preke, Profilis, Krepselis, KrepselioEilutes


class PrekeAtsiliepimasForm(forms.ModelForm):
    class Meta:
        model = Atsiliepimas
        fields = ('turinys', 'preke', 'vertintojas')
        widgets = {  # paslepiam laukus, kad būtų nevaizduojami formoje
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),

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
