# Generated by Django 5.1.5 on 2025-02-23 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0007_orderdetails_od_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetails',
            name='order',
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='od_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
