# Generated by Django 3.2.4 on 2021-07-02 18:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComplaintDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_mobile', models.CharField(max_length=100)),
                ('invoice_number', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('service_requirement', models.TextField()),
                ('customer_address', models.TextField()),
                ('requested_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('technician_assigned', models.CharField(blank=True, max_length=100, null=True)),
                ('current_technician', models.CharField(blank=True, max_length=100)),
                ('diagnosis_description', models.TextField(blank=True)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('material_purchased', models.TextField(blank=True)),
                ('price_of_materials', models.CharField(blank=True, max_length=10)),
                ('price_charged', models.CharField(blank=True, max_length=10)),
                ('payment_advance', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]
