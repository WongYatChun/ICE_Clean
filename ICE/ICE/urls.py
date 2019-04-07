"""ICE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from courses.views import CourseListView


from django.conf import settings
from django.conf.urls.static import static

""" we want to display the list of courses in the URL
http://127.0.0.1:8000/ and all other URLs for the courses application have
the /course/ prefix. """

urlpatterns = [
    # allauth
    path('accounts/',include('allauth.urls')),
    # myaccount
    path('myaccounts/', include('myaccount.urls')),
    # include log-in page
    path('accounts/login/', auth_views.LoginView.as_view(),name='login'),
    # incldue log-out page
    path('accounts/logout/',auth_views.LogoutView.as_view(), name = 'logout'),
    path('admin/', admin.site.urls),
    # include the URL patterns of the courses application
    path('course/', include('courses.urls')),
    # display the login page in the URL http://127.0.0.1:8000/ and other URLs for the course application have the /course/ prefix
    # path('', auth_views.LoginView.as_view(),name='login'),
    path('', CourseListView.as_view(), name='course_list'),
    # include the URL patterns of the students application
    path('students/', include('students.urls')),
    # include the API patterns
    path('api/', include('courses.api.urls', namespace='api')),
    # path('invitations/', include('invitations.urls', namespace='invitations')),
    path('invitations/', include('invitations.urls', namespace='invitations')),
]

""" The Django development server will be in charge of serving the mediafiles during development 
(that is, when the DEBUG setting is set to True ). """

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)