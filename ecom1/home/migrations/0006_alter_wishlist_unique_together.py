# Generated by Django 5.1.3 on 2024-12-15 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_merge_20241214_2042'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together=set(),
        ),
    ]