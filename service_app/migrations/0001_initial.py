# Generated by Django 5.1.3 on 2025-03-18 05:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_provider_image')),
                ('password', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('latitude', models.DecimalField(decimal_places=7, default=0.0, max_digits=11)),
                ('longitude', models.DecimalField(decimal_places=7, default=0.0, max_digits=11)),
                ('is_approved', models.BooleanField(default=False)),
                ('status', models.CharField(default='services_not_added', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.category')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.tblservice')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_app.serviceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_start', models.TimeField()),
                ('slot_end', models.TimeField()),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_app.serviceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAvailableTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_booked', models.BooleanField(default=False)),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_provider_available_time', to='service_app.serviceprovider')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_app.timeslot')),
            ],
        ),
    ]
