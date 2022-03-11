from django.db import models
from django.utils import timezone


class ComplaintDetail(models.Model):
    # Form fields
    customer_name = models.CharField(max_length=100, blank=False)
    customer_mobile = models.CharField(max_length=100, blank=False)
    # customer_mobile = models.IntegerField(null=False, default=00)
    invoice_number = models.CharField(max_length=100, default=None, null=True, blank=True)
    service_requirement = models.TextField(null=False)
    customer_address = models.TextField(null=False)

    # Non-Form Fields
    requested_date = models.DateTimeField(default=timezone.now)
    technician_assigned = models.CharField(max_length=100, null=True, blank=True)
    technician_mobile = models.CharField(max_length=100, blank=False, default='na')

    current_technician = models.CharField(max_length=100, blank=True)

    diagnosis_description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('Just Arrived', 'Just Arrived'), ('On Going','On Going'), ('Closed','Closed'), ('Pending','Pending')], default='Just Arrived')
    material_purchased = models.TextField(blank=True)
    price_of_materials = models.CharField(max_length=10, blank=True)
    price_charged = models.CharField(max_length=10, blank=True)
    payment_advance = models.CharField(max_length=10, blank=True)




