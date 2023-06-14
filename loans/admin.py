from django.contrib import admin
from .models import *
from django import forms
# Register your models here.
admin.site.register(Loan_Type)
# admin.site.register(Loans)
admin.site.register(Documents)
admin.site.register(Document_Status)
admin.site.register(documentType)
admin.site.register(Loan_Status)
admin.site.register(LoanRepayment)

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loans
        fields = '__all__'
        widgets = {
            'guarantors': forms.CheckboxSelectMultiple
        }

class LoanAdmin(admin.ModelAdmin):
    form = LoanForm

admin.site.register(Loans, LoanAdmin)