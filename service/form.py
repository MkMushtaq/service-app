from django import forms
from .models import ComplaintDetail
from django.forms import TextInput, Textarea


class ComplaintRequestForm(forms.ModelForm):
    class Meta:
        model = ComplaintDetail
        fields = ['customer_name', 'customer_mobile', 'invoice_number', 'service_requirement', 'customer_address']

        widgets = {
            'customer_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Mr ABCD'
            }),

            'customer_mobile': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 9999988888'
            }),

            'invoice_number': TextInput(attrs={
                'class': 'form-control',
            }),

            'service_requirement': Textarea(attrs={
                'class': 'h-20 d-inline-block form-control',
            }),

            'customer_address': Textarea(attrs={
                'class': 'h-20 d-inline-block form-control',
            }),
        }
