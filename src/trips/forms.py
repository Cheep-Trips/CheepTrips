from django import forms

class WelcomeForm(forms.Form):
    departure = forms.CharField(
        max_length=256, 
        label="Flying from")
    departure_date = forms.DateField(
        label='Departing')
    return_date = forms.DateField(
        label='Returning')
class DestinationForm(forms.Form):
    departure = forms.CharField(
        max_length=256, 
        label="Flying from")
    arrival = forms.CharField(
        max_length=256, 
        label="Flying to",
        required=False)
    departure_date = forms.DateField(
        label='Departing')
    return_date = forms.DateField(
        label='Returning')
    price_max = forms.IntegerField(
        label='Maximum Cost'
    )
    region = forms.ChoiceField(
        label='Regions',
        required=False,
        choices=[('all', 'All Regions'), ('NA', 'North America'), ('SA', 'South America'), ('EU', 'Europe'), ('AS', 'Asia'), ('AF', 'Africa'), ('AU', 'Australia')]
    )
    activity = forms.ChoiceField(
        label='Activities',
        required=False,
        choices=[('all', 'All Activites'), ('swimming', 'Swimming'), ('surfing', 'Surfing'), ('scenery', 'Scenery'), ('shopping', 'Shopping')]
    )
    travelers = forms.IntegerField(
        label='Travelers',
        initial=1,
        min_value=1
    )
    priority = forms.ChoiceField(
        label='Priority',
        choices=[('cheapest', 'Prioritize Cheapest Flights'), ('fastest', 'Prioritize Fastest Flights')]
    )
