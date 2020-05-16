from django import forms


class WelcomeForm(forms.Form):
    departure = forms.CharField(
        max_length=256, 
        label="Flying from")
    departure_date = forms.DateField(
        label='Departing')
    return_date = forms.DateField(
        label='Returning')
    inspire_me = forms.ChoiceField(
        label='inspire',
        choices=[('yes', 'Inspire Me!'), ('no', 'Specify Destination')]
    )
