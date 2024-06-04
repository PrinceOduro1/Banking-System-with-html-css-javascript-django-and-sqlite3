from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class BankUser(models.Model):
    username = models.CharField(primary_key=True,max_length=10000)
    email = models.EmailField()
    pin = models.CharField(max_length=4)
    initial_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Transaction(models.Model):
    t_choices=[('Withdrawal','withdrawal'),
               ('Deposit','deposit'),
               ('Transfer In','transfer In'),
               ('Transfer Out','transfer Out')]
    bank_user = models.ForeignKey(BankUser,on_delete=models.CASCADE,to_field='username',db_column='username')
    transaction_type = models.CharField(max_length=100,choices=t_choices)
    amount = models.DecimalField(max_digits=100,decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)