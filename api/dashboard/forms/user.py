from  django import  forms

from apps.accounts.models import Account


class UserEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'username', 'bio','password']
