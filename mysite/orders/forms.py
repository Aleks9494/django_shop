from django import forms
from .models import Order


# создание формы, связанной с таблицей
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city']
