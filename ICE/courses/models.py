# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class Category(models.Model):
    # Each course belongs to one of the 6 catergories
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique =True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    # Course
    owner = models.ForeignKey(User,
                              related_name= 'courses_create_time',
                              on_delete = models.CASCADE)
    category = models.ForeignKey(Category, related_name='courses',on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    slug = models.SlugField(max_length=200, unique = True)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    # Student: many-to-many relationship between the Course and User models
    students = models.ManyToManyField(User, 
                                     related_name='courses_joined',
                                     blank = True)

    class Meta:
        ordering = ['create_time']
    
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField(blank=True)
    # Specify the ordering is calculated w.r.t the course by setting `for_fields=['course']`
    #   The order for a new module will be assigned adding 1 to the last module of the same Course object
    order = OrderField(blank = True, for_fields=['course'])

    class Meta: # default ordering
        ordering = ['order']

    def __str__(self):
        return '{}.{}'.format(self.order, self.title)

class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents',on_delete = models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete = models.CASCADE,
                                     limit_choices_to= {'model__in':('text',
                                                                     'image',
                                                                     'video',
                                                                     'file')})
    # Set up a generic relation to associate objects from different models that represent 
    # different types of content:
    #   content_type: A `ForeignKey` field to the ContentType model
    #   object_id: A `PositiveIntegerField` to store the primary key of the related object
    #   item: A `GenericForeignKey` field to the related object by combining the two previous field
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    # Specify the ordering is calculated w.r.t the module by setting `for_fields=['module']`
    #   The order for a new content will be assigned adding 1 to the last content of the same Module object
    order = OrderField(blank = True, for_fields=['module'])

    class Meta: # default ordering
        ordering = ['order']
    

class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name= '%(class)s_related', on_delete = models.CASCADE)
    title = models.CharField(max_length = 250)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now = True)

    def render(self):
        """ 
        provide a common interface to render each type of content 
        
        render_to_string(): 
            1. render a template 
            2. return the rendered content as a string
            Each kind of content is rendered using a template named after the content model.

        self._meta.model_name:
            generate the appropriate template name for each content model dynamically
        """
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class File(ItemBase):
    file = models.FileField(upload_to= 'files')

class Video(ItemBase):
    url = models.URLField()


