from django import forms
from django.core.exceptions import ValidationError

from django_registration.forms import RegistrationForm
from django_select2 import forms as s2forms

from .models import User, Location
import datetime

class WelcomeForm(forms.Form):
    departure = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label='Flying from',
        widget=s2forms.ModelSelect2Widget(
            model=Location,
            search_fields=['airport__icontains', 'city__icontains', 'country__icontains', 'state__icontains'],
            )
    )
    # departure = forms.CharField(
    #     max_length=256, 
    #     label="Flying from")
    departure_date = forms.DateField(
        label='Departing')
    return_date = forms.DateField(
        label='Returning')
    def clean(self):
        if(self.cleaned_data['departure_date'] <= datetime.date.today()):
            raise forms.ValidationError(u'Wrong Date or Time!')


class DestinationForm(forms.Form):
    departure = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label='Flying from',
        widget=s2forms.ModelSelect2Widget(
            model=Location,
            search_fields=['airport__icontains', 'city__icontains', 'country__icontains', 'state__icontains'],
            )
    )
    arrival = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label='Flying to',
        widget=s2forms.ModelSelect2Widget(
            model=Location,
            search_fields=['airport__icontains', 'city__icontains', 'country__icontains', 'state__icontains'],
            ), 
        required=False
    )
    # arrival = forms.CharField(
    #     max_length=256, 
    #     label="Flying to",
    #     required=False)
    departure_date = forms.DateField(
        label='Departing')
    return_date = forms.DateField(
        label='Returning',
        required=False)
    daily_budget = forms.ChoiceField(
        label='Budget',
        required=False,
        choices=[('value_budget', 'Low'), ('value_midrange', 'Medium'), ('value_luxury', 'High')]
    )
    region = forms.ChoiceField(
        label='Regions',
        required=False,
        choices=[('', 'All Regions'), ('North America', 'North America'), ('South America', 'South America'), ('Europe', 'Europe'), ('Asia', 'Asia'), ('Africa', 'Africa'), ('Oceania', 'Oceania')]
    )
    activity = forms.ChoiceField(
        label='Activities',
        required=False,
        choices=[('', 'All Activites'), ("Skiing/Snowboarding","Skiing/Snowboarding"), ('swimming', 'Swimming'), ('surfing', 'Surfing'), ('scenery', 'Scenery'), ('shopping', 'Shopping')]
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

    flight_type = forms.ChoiceField(
        label='One Way or Round Trip',
        choices=[('1', 'One Way'), ('2', 'Round Trip')]
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


class TripNameForm(forms.Form):
    name = forms.CharField(
        max_length=256, 
        label="Name")


class NewAccountForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
    