from django import forms
from .models import UserProfile
from django.contrib.auth.models import Group

class ProfileForm(forms.Form):

    first_name = forms.CharField(label = 'First Name', max_length = 50, required = False)
    last_name = forms.CharField(label = 'Last Name', max_length = 50, required = False)

    telephone = forms.CharField(label='Telephone', max_length = 50, required = False)

class SignupForm(forms.Form):

    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        group = Group.objects.get(name = 'Learner')
        # group = Group.objects.get(name = 'Instructor')
        user.groups.add(group)
        user.save()
        user.profile.save()