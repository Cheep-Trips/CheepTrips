from django import forms


class WelcomeForm(forms.Form):
    departure = forms.CharField(max_length=256, label="Flying from")
    destination = forms.CharField(max_length=256, required=False, label="Flying to")
    departure_date = forms.DateField(label='Departing')
    return_date = forms.DateField(label='Returning')
