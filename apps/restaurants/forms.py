import decimal
from django import forms
from mptt.forms import TreeNodeChoiceField

from apps.core.models import CustomUser
from apps.restaurants.models import Products, FoodImage, Category


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


class ProductsForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='Nome do Produto',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
            }
        )
    )
    description = forms.CharField(
        label='Descrição/Modo de Preparo',
        widget=forms.Textarea(
            attrs={
                'cols': 80,
                'rows': 2,
                
            }
        )
    )
    price = forms.CharField(
        required=True,
        label='Preço',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'value': '',
            }
        )
    )
    class Meta:
        model = Products
        fields = ('name', 'description', 'price')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price:
            price = price.replace('.', '').replace(',', '.')
            try:
                price = decimal.Decimal(price)
            except decimal.DecimalException:
                raise forms.ValidationError("Preço inválido.")
        return price


class FoodImageForm(forms.ModelForm):
    class Meta:
        model = FoodImage
        fields = ['image']


class CategoryForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=Category.objects.all(), 
        level_indicator='──', 
        label='Subcategoria de:',
        required=False
    )
    class Meta:
        model = Category
        fields = ['name', 'parent']
        labels = {
            'parent': 'Subcategoria de:'
        }


class SelectCategoryForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=Category.objects.all(), 
        level_indicator='──', 
        label='Categorias:'
    )
    class Meta:
        model = Category
        fields = ['parent']
