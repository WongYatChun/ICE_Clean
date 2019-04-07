from rest_framework import serializers
from ..models import Category, Course, Module, Content

class CategorySerializer(serializers.ModelSerializer):
    
    """ This is the serializer for the Category model """
    
    class Meta:
        """ Specify the model to serialize and the fields to be included for serialization """
        model = Category
        fields = ['id', 'title', 'slug']

class ModuleSerializer(serializers.ModelSerializer):
    """ This is the serializer for the Module model """
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    """ This is the serializer for the Course model """
    
    # add a module attribute to CourseSerializer to next the ModuleSerializer serializer
    #   many = True: serialize multiple objects
    #   read_only = True: the field is read-only and should not be included in any input to create or update objects

    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course 
        fields = ['id', 'category', 'title', 'slug', 'description',
                  'create_time', 'owner', 'modules']

class ItemRelatedField(serializers.RelatedField):
    """
    In this code, we define a custom field by subclassing the RelatedField serializer field provided by REST framework 
    and overriding the to_representation() method.

    Content model includes a generic foreign key that allows us to associate objects of different content models 
    We have added a common `render()` method for all content models in the previous chapter
        -   Use this method to provide rendered contents to our API

    """


    def to_representation(self, value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    """ define the ContentSerializer serializer for the Content model 
    and use the custom field for the item generic foreign key. """

    item = ItemRelatedField(read_only = True)

    class Meta:
        model = Content
        fields = ['order', 'item']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'category', 'title', 'slug', 'description', 'create_time', 'owner', 'modules']