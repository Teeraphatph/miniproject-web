# Generated by Django 5.1 on 2024-10-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
