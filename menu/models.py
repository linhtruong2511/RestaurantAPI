from random import choices

from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    name = models.CharField()
    def __str__(self):
        return self.name
class MenuItem(models.Model):
    OUT_OF_STOCK = 'oos'
    AVAILABLE = 'ava'
    MENU_STATUS = {
        OUT_OF_STOCK: "out of stock",
        AVAILABLE: "available"
    }
    name = models.CharField()
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')
    status = models.CharField(choices=MENU_STATUS, default='ava')
    image = models.ImageField(upload_to='menu_item', null=True, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name