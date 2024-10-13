# Generated by Django 5.1 on 2024-10-12 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='default_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.address'),
        ),
    ]
