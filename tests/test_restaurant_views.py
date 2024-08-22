import base64
from io import BytesIO
import os
from unittest import mock
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django import forms as frm
import pytest

from apps.restaurants import models
from apps.restaurants import forms
from apps.restaurants import views

from .fixtures import (
    valid_image_data, image_file, 
    product, category
)


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
        argvalues=[('form', forms.ProductsForm)]
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

    def test_upload_product_image_authenticated_post(self, product):
        self.c.force_login(self.u)
        url = reverse('add-image-product', kwargs={'product_id': product.id})
        data = {
            'image_data': 'test_image_data',
            'some_other_field': 'value'
        }
        res = self.c.post(url, data)

        assert res.status_code == 200
        assert res.context['product'].name == 'Test Product'

    @mock.patch('utils.images.compress_image')
    def test_upload_product_image_authenticated_message(
        self, 
        mock_compress_image, 
        image_file, 
        product
    ):
        self.c.force_login(self.u)
        url = reverse('add-image-product', args=[product.id])
        image_file.seek(0)
        image_content = image_file.read()
        compressed_image_file = BytesIO(image_content) 
        compressed_image_file.name = "compressed_image.jpeg"
        mock_compress_image.return_value = compressed_image_file

        image_data = 'data:image/jpeg;base64,' \
            + base64.b64encode(image_content).decode()
        image_file.seek(0)

        uploaded_file = SimpleUploadedFile(
            name=image_file.name,
            content=image_content,
            content_type='image/jpeg'
        )
        data = {
            'image': image_file,
            'image_data': image_data
        }
        files = {
            'image': uploaded_file,
        }

        response = self.c.post(url, data=data, files=files)
        messages = list(get_messages(response.wsgi_request))
        expected_message = 'Imagem para Test Product adicionado com sucesso!'

        assert response.status_code == 200
        assert any(expected_message in str(message) for message in messages)

    def test_upload_product_image_not_authenticated_redirect(self, product):
        url = reverse('add-image-product', args=[product.id])
        res = self.c.get(url)

        assert res.status_code == 302
        assert res.url == 'accounts/login/?next=/restaurants/image-product/new/1'

    def test_create_products_form_is_empty(self, product):
        self.c.force_login(self.u)
        res = self.c.get(reverse('add-image-product', args=[product.id]))
        form = forms.FoodImageForm(instance=product)

        assert res.context['form'].is_bound == False
        assert res.context['form'].is_bound == form.is_bound
        assert res.context['form'].instance == product
        assert isinstance(res.context['form'], forms.FoodImageForm)

    def test_create_products_forms_is_empty(self):
        self.c.force_login(self.u)
        res = self.c.get(reverse('products-new'))
        form = forms.FoodImageForm()

        assert res.context['form'].is_bound == False
        assert res.context['form'].is_bound == form.is_bound

    def test_create_product_valid_form(self):
        self.c.force_login(self.u)
        post_data = {
            'name': 'Product1',
            'description': 'description1',
            'price': '3.23',
        }
        res = self.c.post(reverse('products-new'), data=post_data)

        assert res.status_code == 200
        assert models.Products.objects.count() == 1
        assert models.Products.objects.last().name == 'Product1'

    def test_add_category_to_product_and_redirection(self, db, product, category):
        self.c.force_login(self.u)
        url = reverse('add-product-category', args=[product.id])
        data = {
            'parent': category.id
        }
        
        res = self.c.post(url, data)
        product = get_object_or_404(models.Products, id=product.id)

        assert res.url == '/'
        assert res.status_code == 302
        assert category.name == str(product.category)

    def test_add_category_from_modal_with_parent(self, db, product, category):
        self.c.force_login(self.u)
        url = reverse('add-category', args=[product.id])
        data = {
            'name': 'Cat1',
            'parent': category.id
        }
        res = self.c.post(path=url, data=data)
        category = get_object_or_404(
            klass=models.Category, 
            id=models.Category.objects.last().id
        )
        assert category.name == 'Cat1'
        assert category.parent.name == 'Category1'

    def test_add_category_from_modal_without_parent(self, db, product):
        self.c.force_login(self.u)
        url = reverse('add-category', args=[product.id])
        data = {
            'name': 'Cat2',
        }
        res = self.c.post(path=url, data=data)
        category = get_object_or_404(
            klass=models.Category, 
            id=models.Category.objects.last().id
        )
        assert category.name == 'Cat2'

    def test_add_category_form_is_empty(self, db, product):
        self.c.force_login(self.u)
        url = reverse('add-category', kwargs={'product_id': product.id})
        print('=-=-=-=>', url)
        res = self.c.get(path=url)
        form = forms.CategoryForm()

        assert res.context['form'].is_bound == False
        assert res.context['form'].is_bound == form.is_bound
        assert isinstance(res.context['form'], forms.CategoryForm)
