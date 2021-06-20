from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    is_customer = forms.BooleanField()
    is_admin = forms.BooleanField()


class VehicleForm(forms.Form):
    plate = forms.CharField()
    model = forms.CharField()
    capacity = forms.IntegerField()


