from django.db import models

# Create your models here.
class Payment(models.Model):
    CARD = 'card'
    E_WALLET = 'e-wallet'
    CASH = 'cash'
    METHOD_STATUS = {
        CARD: 'card',
        E_WALLET: 'e-wallet',
        CASH: 'cash'
    }
    order = models.OneToOneField(to='order.Order', on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    method = models.CharField(choices=METHOD_STATUS, default='cash')
    paid = models.BooleanField(default=False)