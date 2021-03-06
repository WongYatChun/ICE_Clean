from django.urls import re_path, path, include
from . import views

app_name = "myaccount"
urlpatterns = [
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
]

