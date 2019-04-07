from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import Course
from .forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    """ The view allow students to register on our site """
    # path of the template
    template_name = 'students/student/registration.html'
    # form for createing objects which has to be `ModelForm`
    #   use Django's UserCreationForm as the registration form to create `User` object
    form_class = UserCreationForm
    # The URL to redirect the user to when the form is succussfully submitted
    #   reverse the `student_course_list` URL
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        """ executed when valid form data has been posted 
        return an HTTP response 
        Override the original method to log the usr in after successfully signing up
        """
        result = super(StudentRegistrationView,
                       self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """ 
    Handle students enrolling in `courses` 
    inherit from:
    `LoginRequiredMixin` mixin 
        -   s.t. only logged-in users can access the view
    `FormView` View:
        -   handle a form submission
    """
    course = None # store the given `Course` object
    form_class = CourseEnrollForm # store the `CourseEnrollForm`

    def form_valid(self, form):
        """ 
        When the form is valid,
         add the current user to the students enrolled in the course 
        """
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView,
                     self).form_valid(form)

    def get_success_url(self):
        """ 
        returns the URL the user will be redirected to if the form was successfully submitted
        -   equivalent to the `success_url` attribute
        """
        # reverse the `student_course_detail` URL to display the course contents
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """ 
    display the courses the students are enrolled in 
    Inherit from:
    -   LoginRequireMixin: only logged in users can access the view
    -   ListView: display a list of `Course` objects    
    """
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        """ override the `get_queryset()
        retrieving only the courses the user is enrolled in """
        qs = super(StudentCourseListView, self).get_queryset()
        # filter the QuerySet by the student's `ManyToManyField`
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    """ 
    A view for accessing the actual course contents  
    """
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        """ 
        override `get_queryset()`
         limit the base QuerySet to courses in which the usr is enrolled 
        """
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        """ 
        override the `get_context_data()`
        student is able to navigate through modules inside a course
        """
        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # set a course module in the context if the `module_id` URL parameter is given
            # get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context
