from untitled2app.forms import Register_Form, Login_Form, BloodForm
from .models import Register_Data, BloodData
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth



def home_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = Register_Form(request.POST)
        if form.is_valid():
            if Register_Data.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, 'register.html', {'form': form, 'error_msg': 'Username already taken.'})
            elif Register_Data.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, 'register.html', {'form': form, 'error_msg': 'Email taken.'})
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                return render(request, 'register.html', {'form': form, 'error_msg': 'passwords not match.'})
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password1']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.mobile = form.cleaned_data['mobile']
                user.save()

                return HttpResponseRedirect('/login/')
    else:
        form = Register_Form()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        lform = Login_Form(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data['username']
            password = lform.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                return HttpResponseRedirect('/choose/')
            else:
                return HttpResponse('non-valid credentials')
    else:
        lform = Login_Form(request.POST)
    return render(request, 'login.html', {'lform': lform})

def data_view(request):
    if request.method == 'POST':
        dform = BloodForm(request.POST)
        if dform.is_valid():
            name = dform.cleaned_data['name']
            age = dform.cleaned_data['age']
            email = dform.cleaned_data['email']
            mobile = dform.cleaned_data['mobile']
            location = dform.cleaned_data['location']
            gender = dform.cleaned_data['gender']
            bloodgroups = dform.cleaned_data['bloodgroups']
            data = BloodData(
                name=name,
                age=age,
                email=email,
                mobile=mobile,
                location=location,
                gender=gender,
                bloodgroups=bloodgroups
            )
            data.save()
            return HttpResponse('Thanks for Submitting Your Details')
        else:
            return HttpResponse('Please donate blood Save Life')
    else:
        dform = BloodForm()
        return render(request, 'blooddonate.html', {'dform': dform})

def donator_list(request):
    data = BloodData.objects.all()
    return render(request, 'donators_data.html', {'data': data})

def contact(request):
    return render(request, 'contact.html')

def choose_site(request):
    return render(request, 'choose.html')
