from django import forms
from .models import Spending, Budget

class SpendingForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ['item_name', 'amount', 'category']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
