# Generated by Django 5.1.3 on 2025-03-20 08:08

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_delete_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=400)),
                ('rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.user')),
            ],
        ),
    ]
