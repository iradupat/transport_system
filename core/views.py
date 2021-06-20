from django.shortcuts import render, redirect
from .forms import RegistrationForm, VehicleForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer, Vehicle, Driver
# Create your views here.


def home_page(request):
    return render(request, 'home_page.html')


def register_account(request):

    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        vehicle_form = VehicleForm(request.POST)
        if reg_form.is_valid():
            try:
                user = User.objects.create_user(username=reg_form.cleaned_data.get('email'),
                                                email=reg_form.cleaned_data.get('email'),
                                                password=reg_form.cleaned_data.get('password'),
                                                first_name=reg_form.cleaned_data.get('first_name'),
                                                last_name=reg_form.cleaned_data.get('last_name'))
            except Exception as e:
                messages.error(request, f"Could not create the account with user name {reg_form.cleaned_data.get('email')}")
                return redirect('home')

            is_admin = reg_form.cleaned_data.get('is_admin')
            if is_admin:
                user.is_staff = True
                user.save()
            else:
                is_customer = reg_form.cleaned_data.get('is_customer')
                if is_customer:
                    try:
                        Customer.objects.create(account=user, phone=reg_form.cleaned_data.get('phone'))
                    except Exception as e:
                        messages.error(request, 'The account was not created, try again latter.')
                else:

                    if vehicle_form.is_valid():
                        try:

                            driver = Driver.objects.create(account=user,
                                                           phone=reg_form.cleaned_data.get('phone'),)

                            Vehicle.objects.create(plate=vehicle_form.cleaned_data.get('plate'),
                                                   model=vehicle_form.cleaned_data.get('model'),
                                                   capacity=vehicle_form.cleaned_data.get('capacity'),
                                                   driver=driver)
                        except Exception as e:
                            messages.error(request, 'Something went wrong, try again latter.')
                    else:
                        messages.error(request, 'Provide the required information please!')
        else:
            messages.error(request, 'Provide the required information please!')

        return render(request, 'home', {"reg_form": reg_form, "vehicle_form": vehicle_form})
    else:
        reg_form = RegistrationForm()
        vehicle_form = VehicleForm()
        return render(request, 'home', {"reg_form": reg_form, "vehicle_form": vehicle_form})