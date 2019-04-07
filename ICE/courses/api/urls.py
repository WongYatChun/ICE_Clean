from django.urls import path, include
from rest_framework import routers
from . import views

""" 
We create a DefaultRouter object and register our view set with the
`course` prefix. The router takes charge of generating URLs automatically for our view set.
"""
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

app_name = 'courses'

urlpatterns = [
     path('categories/',
          views.CategoryListView.as_view(),
          name='category_list'),
     path('categories/<pk>/',
          views.CategoryDetailView.as_view(),
          name='category_detail'),
     path('', include(router.urls)),
]

