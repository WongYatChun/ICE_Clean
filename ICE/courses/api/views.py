from rest_framework import generics, viewsets
from rest_framework.decorators import detail_route
from ..models import Category, Course
from .serializers import CategorySerializer, CourseSerializer

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEnrolled
from .serializers import CourseWithContentsSerializer

""" 

include a pk URL parameter for the detail view to retrieve the object for the given primary key 

Both views have the following attributes:
-   queryset: The base QuerySet to use to retrive objects
-   serializer_class: The class to serialize objects
"""

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ subclass ReadOnlyModelViewSet , 
    provides the read-only actions list() and retrieve() to both list objects or retrieve a single object.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    """ 
    1. We use the detail_route decorator of the framework to specify
        that this is an action to be performed on a single object.
    2. The decorator allows us to add custom attributes for the
        action. We specify that only the post method is allowed for
        this view and set the authentication and permission classes.
    3. We use self.get_object() to retrieve the Course object.
    4. We add the current user to the students many-to-many
        relationship and return a custom success response.
    """

    @detail_route(methods=['post'],
                    authentication_classes=[BasicAuthentication],
                    permission_classes=[IsAuthenticated])
    
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    """ 
    use the detail_route decorator to specify that this action is performed on a single object.

    specify that only the GET method is allowed for this action.

    use the new CourseWithContentsSerializer serializer class that includes rendered course contents.

    use both the IsAuthenticated and our custom IsEnrolled permissions. 
    By doing so, we make sure that only users enrolled in the course are able to access its contents.

    use the existing retrieve() action to return the Course object
    """
    @detail_route(methods=['get'],
                    serializer_class=CourseWithContentsSerializer,
                    authentication_classes=[BasicAuthentication],
                    permission_classes=[IsAuthenticated,IsEnrolled])
    
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)