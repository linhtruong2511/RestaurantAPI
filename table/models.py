from email.policy import default
from random import choices

from django.db import models


# Create your models here.
class Table(models.Model):
    number = models.IntegerField()
    is_busy = models.BooleanField(default=False)
    order = models.ManyToManyField("order.Order", related_name='tables', blank=True, null=True)

    def __str__(self):
        return "number of table: " + str(self.number)
