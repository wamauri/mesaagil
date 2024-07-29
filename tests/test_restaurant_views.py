import os
from unittest import mock
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django import forms as frm
import pytest

from apps.restaurants import models
from apps.restaurants import forms

from .fixtures import valid_image_data, image_file


@pytest.mark.django_db
class TestRestaurantViews:

    def setup_method(self) -> None:
        self.c = Client()
        self.credentials = {
            'email': 'test@test.com',
            'password': '12345678',
        }
        self.u = get_user_model().objects.create_user(**self.credentials)
        self.img_path = 'media/food_images/compressed_image.jpeg'
        self.compressed_image = Path(self.img_path)

    def teardown_method(self):
        get_user_model().objects.all().delete()
        models.Products.objects.all().delete()
        models.FoodImage.objects.all().delete()
        if self.compressed_image.exists():
            os.remove(self.img_path)

    @pytest.mark.parametrize(
        argnames='url, expected', 
        argvalues=[('products-new', '/products/new/'), ('waiters-new', '/waiters/new/')]
    )
    def test_create_waiters_products_redirect_if_not_logged_in(self, url, expected):
        response = self.c.get(reverse(url))
        assert response.status_code == 302
        assert response.url.endswith(expected)

    @pytest.mark.parametrize(
        argnames='type_form, form_expected', 
        argvalues=[('pform', forms.ProductsForm), ('iform', forms.FoodImageForm),]
    )
    def test_create_waiters_products_forms_is_empty(self, type_form, form_expected):
        self.c.force_login(self.u)
        response = self.c.get(reverse('products-new'))
        form = form_expected()
        assert response.context[type_form].is_bound == form.is_bound

    def test_form_products_validation_error_field_price(self):
        form = forms.ProductsForm({
            'name': 'Name',
            'description': 'Decription',
            'price': 'wyzx',
        })
        assert isinstance(form.errors.as_data()['price'][0], frm.ValidationError)

    @mock.patch('utils.images.compress_image')
    def test_create_product_success(self, mock_compress, valid_image_data, image_file):
        self.c.force_login(self.u)

        image_file.seek(0)
        mock_compress.return_value = SimpleUploadedFile(
            "compressed_image.jpg", 
            b"file_content", 
            content_type="image/jpeg"
        )

        post_data = {
            'name': 'Test Product',
            'description': 'Description',
            'price': 99.99,
            'tags': 'tag1,tag2',
            'image': image_file,
            **valid_image_data
        }
        image_file.seek(0)
        files = {
            'image': image_file,
        }

        response = self.c.post(reverse('products-new'), data=post_data, files=files)

        assert response.status_code == 200
        assert models.Products.objects.count() == 1
        assert models.FoodImage.objects.count() == 1

        product = models.Products.objects.first()
        assert product.name == 'Test Product'
        assert 'TAG1' in product.category.values_list('name', flat=True)
        assert 'TAG2' in product.category.values_list('name', flat=True)
        assert product.food_image is not None

    @mock.patch('utils.images.compress_image')
    def test_create_product_invalid_form(self, valid_image_data, image_file):
        self.c.force_login(self.u)
        
        post_data = {
            'name': '',
            'tags': 'tag1,tag2',
            **valid_image_data
        }

        image_file.seek(0)
        files = {
            'image': image_file,
        }
        
        response = self.c.post(reverse('products-new'), data=post_data, files=files)
        
        assert response.status_code == 200
        assert models.Products.objects.count() == 0
        assert models.FoodImage.objects.count() == 0
        assert b'Algo deu errado ao criar produto!' in response.content
