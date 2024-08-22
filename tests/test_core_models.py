import os

import pytest

from apps.core.models import CustomUser
from apps.restaurants.models import FoodImage, Products, Category
from .fixtures import image, user, image_file, category


class TestCoreModels:
    def setup_method(self, method):
        self.pw = "12345678"
        self.email = "test@test.com"

    def test_customuser_model_str_method(self, django_user_model):
        user = django_user_model.objects.create(
            email=self.email,
            password=self.pw,
        )
        assert str(user) == self.email

    def test_customuser_create_user_without_email_raises_an_valueerror(self, django_user_model):
        with pytest.raises(ValueError):
            django_user_model.objects.create_user(
                email=None,
                password=self.pw,
        )

    def test_customuser_creates_instance(self, django_user_model):
        user = django_user_model.objects.create_user(
            email=self.email,
            password=self.pw,
        )
        assert isinstance(user, CustomUser)

    def test_customuser_create_super_user_setting_isstaff_to_false_raises_valueerror(self, django_user_model):
        with pytest.raises(ValueError):
            django_user_model.objects.create_superuser(
                email=self.email,
                password=self.pw,
                is_staff=False
            )

    def test_customuser_create_super_user_setting_issuperuser_to_false_raises_valueerror(self, django_user_model):
        with pytest.raises(ValueError):
            django_user_model.objects.create_superuser(
                email=self.email,
                password=self.pw,
                is_superuser=False
            )

    def test_customuser_create_superuser(self, django_user_model):
        user = django_user_model.objects.create_superuser(
            email=self.email,
            password=self.pw,
        )
        assert user.is_superuser == True
        assert user.is_staff == True

    def test_product_model_str_method(self, category, user):
        product = Products.objects.create(
            category=category,
            name='Porção de Carne do Sol',
            description='Descrição da porção de carne do sol',
            price='99.99',
            user=user,
        )
        assert str(product) == 'Porção de Carne do Sol'
        assert product.description == 'Descrição da porção de carne do sol'

    def test_food_image_str_method(self, image_file):
        food_image = FoodImage(image=image_file)
        assert str(food_image) == 'preview.jpg'
