from django import forms
from courses.models import Course

""" Create functionality for students to enroll in courses """

class CourseEnrollForm(forms.Form):
    """ for students to enroll in courses """
    # HiddenInput because we are not going to show thie field to the user
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
    # use this form in the `CourseDetailView` view to display a button to enroll
    
