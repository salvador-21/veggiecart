# Generated by Django 5.1.5 on 2025-02-23 22:08

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0004_transferhistory_t_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, related_name='od_poduct', to='storeapp.order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_status',
            field=models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('OUT OF STOCK', 'OUT OF STOCK'), ('UNAVAILABLE', 'UNAVAILABLE')], default='UNAVAILABLE', max_length=50),
        ),
    ]
