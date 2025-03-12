from datetime import datetime, timezone

from django.db import models
from django.template.defaultfilters import default
from django.utils import timezone
from menu.models import MenuItem
from users.models import Customer


# Create your models here.
class OrderItem(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True, related_name='order_items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.menu_item} : {self.quantity}'


class Order(models.Model):
    PENDING = "Pending"
    IN_PROGRESS = "In progress"
    COMPLETED = "Complete"
    CANCELLED = "Cancelled"
    STATUS_CHOICE = {
        PENDING: "pending",
        IN_PROGRESS: "in_progress",
        COMPLETED: "completed",
        CANCELLED: "cancelled"
    }

    order_date = models.DateTimeField(default= timezone.now)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        choices=STATUS_CHOICE,
        default=PENDING
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    take_away = models.BooleanField(default=False)
    menu_item = models.ManyToManyField(to='menu.MenuItem', related_name='orders', through=OrderItem)

    class Meta:
        ordering = ['-order_date', '-id']
