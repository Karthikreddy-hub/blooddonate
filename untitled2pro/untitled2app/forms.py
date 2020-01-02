from django import forms
from .models import Login_Data
from django.contrib.auth.models import User
from multiselectfield import MultiSelectFormField

class Register_Form(forms.ModelForm):
    mobile= forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'})   )
    class Meta():
        model= User
        fields=['first_name','last_name','email', 'username']

class Login_Form(forms.ModelForm):
    class Meta():
        model= Login_Data
        fields= '__all__'
class BloodForm(forms.Form):
    name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    age= forms. IntegerField(widget= forms.NumberInput(attrs={'class':'form-control'}))
    email= forms. EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile= forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    location= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    GENDER_CHOICES=(
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender=forms.ChoiceField(widget=forms.RadioSelect(), choices=GENDER_CHOICES)
    BLOOD_GROUPS=(
        ('A-', 'A NAGATIVE'),
        ('A+', 'A POSITIVE'),
        ('B-', 'B NAGATIVE'),
        ('B+', 'B POSITIVE'),
        ('AB-', 'AB NAGATIVE'),
        ('AB+', 'AB POSITIVE'),
        ('O-', 'O NAGATIVE'),
        ('O+', 'O POSITIVE')
    )
    bloodgroups= MultiSelectFormField(max_length=100, choices=BLOOD_GROUPS, label='Select Your Bloodgroup')
