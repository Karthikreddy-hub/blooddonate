from django .db import models
from multiselectfield import MultiSelectField

class Register_Data(models.Model):
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    username= models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile= models.BigIntegerField()
    password1= models.CharField(max_length=100)
    password2= models.CharField(max_length=100)
    def __unicode__(self):
        return self.username
class Login_Data(models.Model):
    username= models.CharField(max_length=100)
    password= models.CharField(max_length=100)

class BloodData(models.Model):
    name= models.CharField(max_length=100)
    age= models.IntegerField()
    email= models.EmailField(max_length=100)
    mobile= models.BigIntegerField()
    location= models.CharField(max_length=100)
    gender= models.CharField(max_length=100)
    BLOOD_GROUPS= (
        ('A-','A NAGATIVE'),
        ('A+','A POSITIVE'),
        ('B-','B NAGATIVE'),
        ('B+','B POSITIVE'),
        ('AB-','AB NAGATIVE'),
        ('AB+','AB POSITIVE'),
        ('O-','O NAGATIVE'),
        ('O+','O POSITIVE')
    )
    bloodgroups= MultiSelectField(max_length=100, choices=BLOOD_GROUPS)
