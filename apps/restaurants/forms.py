from django import forms

from apps.core.models import CustomUser


class WaiterForm(forms.ModelForm):
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'exemplo@exemplo.com'
            }
        )
    )
    full_name = forms.CharField(
        label='Nome Completo',
        widget=forms.TextInput(
            attrs={
                'label': 'Nome Completo',
                
            }
        )
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'off', 
                'required': True,
                'placeholder': 'Senha do Garçon'
            }
        )
    )
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password')
