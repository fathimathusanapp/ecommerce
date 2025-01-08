# Generated by Django 5.1.3 on 2025-01-01 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_order_user_remove_orderline_order_and_more'),
        ('payment', '0005_alter_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.coupon'),
        ),
    ]