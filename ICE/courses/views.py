from django.shortcuts import render

# Create your views here.

# Create class-based views

""" 
When you need to provide a specific behaviour for several class-based views,
it is recommended to use mixins

Mixins are a special kind of multiple inheritance for a class
-   Provide common discrete functionality that added to other mixins
-   Allow you to define the behaviour of a class
Two main situations:
-   provide multiple optinal features for a class
-   use a particular feature in the several classes

Restrict access to class-based views
-   LoginRequiredMixin: Replicate the `login_required` decorator's functionality
-   PermissionRequiredMixin: Grant access to the view to users that have a specific permission.
    -   check the use accessing the view has the permission specified in the `permission_required` attribute
"""
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.forms import inlineformset_factory
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Category, Content, Course
from django.db.models import Count

from django.views.generic.detail import DetailView

from students.forms import CourseEnrollForm

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from django.views.generic.detail import DetailView

from django.core.cache import cache
from django.contrib import messages

class OwnerMixin(object):
    # Used for views that interact with any model that contains an owner attribute
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner = self.request.user)

class OwnerEditMixin(object):
    # override this method to automatically 
    #   set the current user in the owner attribute of the object being saved
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin,self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['category', 'title', 'slug', 'description']
    success_url = reverse_lazy('manage_course_list')

## ---------------- Course -----------------------------------
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['category', 'title', 'slug', 'description']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin,
                        OwnerCourseEditMixin, UpdateView):
    # Allow editting an existing `Course` object
    permission_required = 'courses.change_course'

class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    # Redirect the user after the object is deleted
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'

#----------------------------- Module-----------------------
class CourseModuleUpdateView(TemplateResponseMixin, View):
    
    """ 
    TemplateResponseMixin:
    take charge of rendering templates and returning an HTTP response
    require a `template_name` attribute that indicates the template to be rendered and 
    provides the render_to_response() method to pass it a context and render the template.

    View:
    The basic class-based view provided by Django
    """
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """ 
        Avoid repeating the code the build the formset
        create a `ModuleFormSet` object with optional data
        """
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        """ 
        provided by the view class
        take an HTTP request and its parameters and attemps to delegate to a lowercase method
        that matches the HTTP method used:
            a GET request is delegated to the `get()` method and a `post` request to `post), respectively
        """
        # retrieve the course for both GET and POST requests
        # save it into the `course` attribute of the view to make it accessible to other method
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        """ Executed for GET request
        Build an empty ModuleFormSet formset and render it to the template 
        together with the current `Course` object using the `render_to_response()`
        method provided by `TemplateResponseMixin`
         """
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})
    
    def post(self, request, *args, **kwargs):
        """ 
        Execute for POST requests
        """
        # 1. Build a `ModuleFormSet` instance using the submitted data
        formset = self.get_formset(data=request.POST)
        # 2. Check if the forms are valid
        if formset.is_valid():
            # 3.1 If valid, save it
            formset.save()
            # 4. Redirect user to the `manage_course_list` URL
            return redirect('manage_course_list')
        # 3.2. If not valid, render the template to display any error
        return self.render_to_response({'course': self.course, 'formset': formset})

# --------------------Content-----------------------

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """ Obtain the actual class for the given model name """
        # Check that the given model name is one of the four content models
        if model_name in ['text','video','image', 'file']:
            return apps.get_model(app_label = 'courses',model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """ Build a dynamic form using the `modelform_factory()` """

        # `exclude` parameter to specify the common fields to exclude from 
        #   the form and let other attributes be included automatically
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'create_date',
                                                 'update_date'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id = None):
        """ receives the URL parameters 
                and stores the corresponding module, model, and content object as class attributes """
        self.module = get_object_or_404(Module, id = module_id, course__owner = request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id = id, owner = request.user)
        return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id = None):
        """ Execute when a GET request is received, 
        build the model for the Text, Video, Image, or File instance that is being updated """
        form = self.get_form(self.model, instance= self.obj)
        # otherwise, we pass no instance to create a new object, since `self.obj` is None if no ID is provided
        return self.render_to_response({'form': form, 'object':self.obj})
    
    def post(self,request, module_id, model_name, id = None):
        """ Execute when a POST request is received """
        
        # build the modelform passing any submitted data
        form = self.get_form(self.model,
                                instance = self.obj,
                                data = request.POST,
                                files = request.FILES)
        
        if form.is_valid():
            # if the form is valid, we create a new object and assign request.user as its ower
            obj = form.save(commit = False)
            obj.owner = request.user
            obj.save()
            if not id: # if no ID is provided, we know the user is creating a new object instead of updating an existing one
                # new content
                Content.objects.create(module = self.module, item = obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})

class ContentDeleteView(View):
    def post(self, request, id):
        """ retrieves the Content object with the given ID; it deletes the related Text , Video , Image , or File object; and finally, 
        it deletes the Content object and redirects the user to the module_content_list URL to list the other contents of the module """
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    """ gets the Module object with the given ID that belongs to the current user 
    and renders a template with the given module. """
    template_name = 'courses/manage/module/content_list.html'
    def get(self, request, module_id):
        module = get_object_or_404(Module,
        id=module_id,
        course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, # avoid checking the CSRF token in the POST request, need this to perform AJAX POST requests without having to generate a csrf_token
                      JsonRequestResponseMixin, # Parse the request data as JSON and Serialize the response as JSON and return an HTTP response with the `application/json` content type
                      View):
    """ A view that receives the new order of modules' ID encoded in JSON 
    Support the drag-n-drop functionality in the template"""
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                                    course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    """ A view that receives the new order of contents' ID encoded in JSON 
    Support the drag-n-drop functionality in the template """
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                    module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    """ 
    course catalog, list all available courses, optionally filtered by categories
    display a single course overview
    """
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, category=None):
        # retrieve all categories, including 
        #   the total number of courses for each of them
        #   cache the queries in our views
        categories = cache.get('all_categories')
        if not categories:
            categories = Category.objects.annotate(total_courses=Count('courses'))
            cache.set('all_categories',categories)
        # retrieve all available courses, including the total number 
        #   of modules contained in each course.
        # cache both all_courses and courses filtered by category
        # `all_courses` cache key for storing all courses if no category is given
        all_courses = Course.objects.annotate(total_modules=Count('modules'))
        if category:
            # If a category (slug URL parameter) is given, 
            #   retrieve the corresponding category object and we limit the query to the 
            #   courses that belong to the given category.
            category = get_object_or_404(Category, slug=category)
            # dynamically build the key
            key = 'category_{}_courses'.format(category.id)
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(category=category)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)

        # render the objects to the template and return an HTTP response
        return self.render_to_response({'categories': categories, 'category': category, 'courses': courses})

# displaying a single course overview

class CourseDetailView(DetailView):
    """ retrieve a single object for the given model. 
    Then, it renders the template specified in template_name , 
    including the object in the context as object. """
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        """ include the enrollment form in the context for rendering the templates """
        context = super(CourseDetailView,self).get_context_data(**kwargs)
        # initialize the hiddencourse field of the form with the current `Course` object
        #   s.t. it can submitted directly
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        return context
