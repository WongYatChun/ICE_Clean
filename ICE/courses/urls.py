""" 
    URL patterns for the list, create, edit, and delete course views.
"""

from django.urls import path
from . import views

urlpatterns = [
      # Display a list for Courses to manage
      path('mine/',
            views.ManageCourseListView.as_view(),
            name='manage_course_list'),
      # The page to create a course
      path('create/',
            views.CourseCreateView.as_view(),
            name='course_create'),
      # The page to update a course
      path('<pk>/edit/',
            views.CourseUpdateView.as_view(),
            name='course_edit'),
      # The page to delete a course
      path('<pk>/delete/',
            views.CourseDeleteView.as_view(),
            name='course_delete'),
      # The page to update a module
      path('<pk>/module/',
            views.CourseModuleUpdateView.as_view(),
            name='course_module_update'),
      # The page to create content
      path('module/<int:module_id>/content/<model_name>/create/',
            views.ContentCreateUpdateView.as_view(),
            name='module_content_create'),
      # The page to update content
      path('module/<int:module_id>/content/<model_name>/<id>/',
            views.ContentCreateUpdateView.as_view(),
            name='module_content_update'),
      # The page the delete content
      path('content/<int:id>/delete/',
            views.ContentDeleteView.as_view(),
            name='module_content_delete'),
      # The page to display the content list
      path('module/<int:module_id>/',
            views.ModuleContentListView.as_view(),
            name='module_content_list'),
      # The page to order the modules
      path('module/order/',
            views.ModuleOrderView.as_view(),
            name='module_order'),
      # The page to order the contents
      path('content/order/',
            views.ContentOrderView.as_view(),
            name='content_order'),
      # display all courses for a category
      path('category/<slug:category>/', 
            views.CourseListView.as_view(),
            name='course_list_category'),
      # display a course overview
      path('<slug:slug>/', 
            views.CourseDetailView.as_view(),
            name='course_detail'),
]