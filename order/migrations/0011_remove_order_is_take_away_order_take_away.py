# Generated by Django 5.1.6 on 2025-02-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_order_options_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_take_away',
        ),
        migrations.AddField(
            model_name='order',
            name='take_away',
            field=models.BooleanField(default=False),
        ),
    ]
