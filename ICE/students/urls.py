from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

""" the result for the StudentCourseDetailView is cached for 15 minutes """


urlpatterns = [
     # register view
     path('register/',
          views.StudentRegistrationView.as_view(),
          name='student_registration'),
     # enrol course view
     path('enroll-course/',
          views.StudentEnrollCourseView.as_view(),
          name='student_enroll_course'),
     # course list view
     path('courses/',
          views.StudentCourseListView.as_view(),
          name='student_course_list'),
     # module list view
     path('course/<pk>/',
          cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
          name='student_course_detail'),
     # content list view
     path('course/<pk>/<module_id>/',
          cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
          name='student_course_detail_module'),
]
