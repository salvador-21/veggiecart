# Generated by Django 5.1.5 on 2025-02-24 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0009_alter_cart_cart_price_alter_order_order_shipping_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_payment',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
