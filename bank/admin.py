from django.contrib import admin
from .models import BankUser,Transaction
# Register your models here.
admin.site.register(BankUser)
admin.site.register(Transaction)