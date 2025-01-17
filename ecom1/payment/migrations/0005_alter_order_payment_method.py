# Generated by Django 5.1.3 on 2025-01-01 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cod', 'Cash on Delivery'), ('stripe', 'Stripe')], default='cod', max_length=20),
        ),
    ]
