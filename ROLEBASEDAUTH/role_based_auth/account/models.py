from django.db import models
from django.contrib.auth.models import AbstractUser,Group
import uuid
# Create your models here.

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)
class User(AbstractUser):
    ROLES = [
        ('Admin','Admin'),
        ('Doctor','Doctor'),
        ('Patient','Patient'),
        ('Staff','Staff')
    ]
    role = models.CharField(max_length=50, choices = ROLES)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # objects = UserManager()

class AdminProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="admin_user")
    admin_id = models.CharField(max_length=50,unique=True)

class DoctorProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="doctor")          
    specialization = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50,unique=True)
    hospital = models.CharField(max_length=300)
    department = models.CharField(max_length=50)
    def __str__(self):
        return self.user.username
    
class PatientProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="patient")  
    medical_history = models.CharField(max_length=300)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=50)
    insurance_number = models.CharField(max_length=50,unique=True,null=True,blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    def __str__(self):
        return self.user.username  
class StaffProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="staff")
    employee_id = models.CharField(max_length=50,unique=True)
    doctor = models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
    
def genrate_map_id():
    return str(uuid.uuid4()).split("-")[0].upper()
    
class Mapping(models.Model):
    mapping_id = models.CharField(max_length=50,default=genrate_map_id,unique=True)
    patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
    remarks = models.CharField(max_length=300)            