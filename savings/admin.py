from django.contrib import admin
from .models import SavingsAccount,ReceiveSavings,WidthdrawSavings
# Register your models here.
admin.site.register(SavingsAccount)
admin.site.register(ReceiveSavings)
admin.site.register(WidthdrawSavings)