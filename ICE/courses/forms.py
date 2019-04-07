from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module
from django.forms.utils import ValidationError
""" 
These groups of forms are known as formsets.
Formsets manage multiple instances of a certain Form or ModelForm . All
forms are submitted at once and the formset takes care of the initial
number of forms to display, limiting the maximum number of
forms that can be submitted and validating all the forms.

Formsets include an is_valid() method to validate all forms at once.
You can also provide initial data for the forms and specify how
many additional empty forms to display.

Inline formsets are a small abstraction on top of formsets that simplify working with
related objects. This function allows us to build a model formset
dynamically for the Module objects related to a Course object.
"""

ModuleFormSet = inlineformset_factory(Course,
                                        Module,
                                        fields = ['title','description'],
                                        extra=1,
                                        can_delete= True)


