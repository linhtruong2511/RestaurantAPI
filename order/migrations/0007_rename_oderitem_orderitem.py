# Generated by Django 5.1.6 on 2025-02-22 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('order', '0006_order_is_take_away'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OderItem',
            new_name='OrderItem',
        ),
    ]
