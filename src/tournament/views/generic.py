from django.db import models
from django.views import generic
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from crispy_forms.helper import FormHelper


class FormHelperMixin(FormMixin):
    helper: FormHelper

    def get_helper(self):
        return FormHelper()

    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.helper = self.get_helper()

        return form_class


class DetailListView(generic.DetailView, MultipleObjectMixin):
    def get_object_list(self):
        pass

    def get_context_object_name(self, obj):
        """Get the name of the item to be used in the context."""
        if isinstance(obj, models.Model):
            return obj._meta.model_name
        elif hasattr(obj, "model"):
            return "%s_list" % obj.model._meta.model_name
        else:
            return None

    def get_context_data(self, **kwargs):
        return super().get_context_data(object_list=self.get_object_list(), **kwargs)
