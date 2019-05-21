from django.contrib.auth.models import AbstractUser 
from django.conf import settings
from django.utils import timezone
from django.db import models 
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from phonenumber_field import formfields
from phonenumber_field.phonenumber import PhoneNumber, to_python, validate_region
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from datetime import datetime



class User(AbstractUser):
    username = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


# Choices = ((1, 'Ногтевой сервис'),
#            (2, 'Макияж'),
#            (3, 'Парикмахер'),
#            (4, 'Массаж'),
#            (5, 'Косметолог'),
#            (6, 'Бровист'),
#            (7, 'Ресницы'),
#            (8, 'Татуаж'),
#            (9, 'Эпиляция'))

# class ServiceType(models.Model):

#     my_field = MultiSelectField(choices=Choices,
#                              min_choices=1)
class ServiceType(models.Model):
    service_type = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'ServiceType'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.service_type

                          

class MasterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
        related_name='profile')
    full_name = models.CharField(max_length=500)
    address = models.CharField(max_length=255)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    profile_photo = models.ImageField(upload_to='uploads', blank=True)
    gallery = models.ImageField(upload_to='uploads', blank=True)
    services = models.ManyToManyField(ServiceType)
    
    

    class Meta:
        verbose_name = 'MasterProfile'
        verbose_name_plural = 'Masters'

    def __str__(self):
        return self.user.email


class Schedule(models.Model):
    master = models.OneToOneField(MasterProfile, on_delete=models.CASCADE, \
        related_name='schedule')
    starttime = models.TimeField()
    endtime = models.TimeField()


class Booking(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null=True, \
        related_name='booking')
    master = models.OneToOneField(MasterProfile, on_delete=models.CASCADE,blank=True, \
        null=True,related_name='book')
    service = models.ManyToManyField(ServiceType, related_name='servtype')
    time = models.TimeField()
    date = models.DateField()
    phonenumber = models.CharField(max_length=300, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    


