from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class WelcomeForm(forms.Form):
    departure = forms.CharField(max_length=256, label="Flying from")
    destination = forms.CharField(max_length=256, required=False, label="Flying to")
    departure_date = forms.DateField(label='Departing', widget=DateInput())
    return_date = forms.DateField(label='Returning', widget=DateInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] = field.widget.attrs['class'] + " form-control mr-sm-2"
            else:
                field.widget.attrs['class'] = "form-control mr-sm-2"
            field.widget.attrs['placeholder'] = field.label