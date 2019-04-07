from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')

    telephone = models.CharField('Telephone', max_length = 50, blank = True)

    mod_date = models.DateTimeField('Last modified', auto_now =True)


    class Meta:
        verbose_name = 'User Profle'
        def __str__(self):
            return "{}'s profile".format(self.__str__())

    
