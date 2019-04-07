from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    """ 
    subclass the BasePermission class
    override the has_object_permission() 
    check that the user performing the request is present in the students relationship of the Course object. 
    use the IsEnrolled permission next. """
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()