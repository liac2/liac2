from django.shortcuts import render
from django import forms


def setup():
    household_choices = {
        '': 'Bitte Wählen'
    }
    for n in range(10):
        n = str(n)
        household_choices[n] = n
    return household_choices
insurance_choices = {
    '': 'Bitte wählen',
    'amb': 'Amb',
    'assura': 'Assura' 
}

class Angebot(forms.Form):
    prior_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Vorname', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nachname', 'class': 'form-control'}))
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class': 'form-control'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Straße', 'class': 'form-control'}))
    plz = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'PLZ', 'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Wohnort', 'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Telefon', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-Mail', 'class': 'form-control'}))
    household = forms.ChoiceField(choices=setup(), widget=forms.Select(attrs={'class': 'form-control'}))
    insurance = forms.ChoiceField(choices=insurance_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    checkbox = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

# Create your views here.
def index(request):
    return render(request, 'web/index.html', {
        'angebot_form': Angebot() 
    })


def traditionel(request):
    return render(request, 'web/traditionell.html')