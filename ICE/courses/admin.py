# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

#Register your models here.
from .models import Category, Course, Module

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug':('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title','category','create_time']
    list_filter = ['create_time','category']
    search_fields = ['title','description']
    prepopulated_fields = {'slug':('title',)}
    inlines = [ModuleInline]