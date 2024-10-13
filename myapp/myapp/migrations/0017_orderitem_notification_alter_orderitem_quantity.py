# Generated by Django 5.1 on 2024-09-26 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='notification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]