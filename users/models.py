from email.policy import default

from django.contrib.auth.models import AbstractUser
from django.db import models

def upload_to(instance, filename):
    return 'avatar/{filename}'.format(filename=filename)

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=10, default='')
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)
    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)


class Employee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
