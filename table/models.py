from email.policy import default
from random import choices

from django.db import models

from order.models import Order


# Create your models here.
class Table(models.Model):
    number = models.IntegerField()
    is_busy = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return "number of table: " + str(self.number)
