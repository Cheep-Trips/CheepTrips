from django import forms
from django.core.exceptions import ValidationError

from django_registration.forms import RegistrationForm
from .models import User
import datetime

class WelcomeForm(forms.Form):
    departure = forms.CharField(
        max_length=256, 
        label="Flying from")
    departure_date = forms.DateField(
        label='Departing')
    return_date = forms.DateField(
        label='Returning')
    def clean(self):
        if(self.cleaned_data['departure_date'] < datetime.date.today()):
            raise forms.ValidationError(u'Wrong Date or Time!')


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
    def clean(self):
        if(self.cleaned_data['departure_date'] < datetime.date.today()):
            print("CLEAN:",self.cleaned_data['departure_date'] < datetime.date.today())
            raise forms.ValidationError(u'Wrong Date or Time!')


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        max_length=256, 
        label="Email",
        widget=forms.EmailInput)

        
class SignInForm(forms.Form):
    email = forms.CharField(
        max_length=256, 
        label="Email",
        widget=forms.EmailInput)
    password = forms.CharField(
        max_length=256, 
        label="Password",
        widget=forms.PasswordInput)

        
class ProfileForm(forms.Form):
    new_password = forms.CharField(
        max_length=256, 
        label="New Password",
        widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        max_length=256, 
        label="Confirm Password",
        widget=forms.PasswordInput)


class NewAccountForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
    