import django_filters
from service.models import ComplaintDetail
from django.forms import TextInput, CharField
from django_filters import DateFilter, CharFilter


class ComplaintFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='requested_date', lookup_expr='gte', label="Start Date")
    end_date = DateFilter(field_name='requested_date', lookup_expr='lte', label="End Date")
    customer_name = CharFilter(field_name='customer_name', lookup_expr='icontains', label='Customer Name')
    current_technician = CharFilter(field_name='current_technician', lookup_expr='icontains', label='Technician Name')

    class Meta:
        model = ComplaintDetail
        fields = ['customer_name', 'status', 'requested_date', 'current_technician']

        # widgets = {
        #     'customer_name': TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Ex: Mr ABCD'
        #     }),
        #
        # }
