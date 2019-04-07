""" 
We need a field that allow us to define an order for objects
-   specify an order for objects using existing Django fields 
        by adding a `PositiveIntegerField` to your model
-   create a custom order field that inherits from `PositiveIntegerField` and provides additional behavior
-   Two relevant functionalities
    -   Automatically assign an order value when no specific order is provided
    -   Order objects with respect to other fields
        -   e.g. Course modules will be ordered w.r.t the course they belong to
        -   e.g. Module contents w.r.t the module they belong to

Tips:
When you create custom model fields, make them generic. Avoid hardcoding
data that depends on a specific model or field. Your field should work in any
model.
"""

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        """ Inherited from `PositiveIntegerField`, takes an optional `for_field` parameter """
        # `for_field` allows us to indicate the fields that the order has to be calculated with respect to
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    # Override the `pre_save()` method of the `PositiveIntegerField`
        # executed before saving the field into the database
    def pre_save(self, model_instance, add):
        # Check if a value already exists for this field in the model instance
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                # build a QuerySet to retrieve all objects for the field's model
                #   retrieve the model class the field belongs to by accessing `self.model`
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                # if no object, assume to be the first one
                value = 0
            setattr(model_instance, self.attname,value)
            return value
        else:
            # if the model instance has a value for the current field, do nothing
            return super(OrderField, self).pre_save(model_instance,add)