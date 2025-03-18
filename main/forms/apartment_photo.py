from django import forms
from . import BaseModelForm
from ..models import ApartmentPhoto

class ApartmentPhotoForm(BaseModelForm):
    class Meta:
        model = ApartmentPhoto
        fields = ['photo']
