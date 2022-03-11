from django.contrib.auth.models import User
from django.forms import ModelForm
from service.models import ComplaintDetail
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CompliantUpdateForm(ModelForm):
    class Meta:
        model = ComplaintDetail
        fields = '__all__'

