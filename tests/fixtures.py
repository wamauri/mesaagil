import base64

import pytest
from django.test import Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.restaurants.models import FoodImage, Products, Category

available_fixtures = [
    "admin_client", 
    "admin_user", 
    "async_client", 
    "async_rf", 
    "cache", 
    "capfd", 
    "capfdbinary", 
    "caplog", 
    "capsys", 
    "capsysbinary", 
    "client", 
    "cov", 
    "db", 
    "django_assert_max_num_queries", 
    "django_assert_num_queries", 
    "django_capture_on_commit_callbacks", 
    "django_db_blocker", 
    "django_db_createdb", 
    "django_db_keepdb", 
    "django_db_modify_db_settings", 
    "django_db_modify_db_settings_parallel_suffix", 
    "django_db_modify_db_settings_tox_suffix", 
    "django_db_modify_db_settings_xdist_suffix", 
    "django_db_reset_sequences", 
    "django_db_serialized_rollback", 
    "django_db_setup", 
    "django_db_use_migrations", 
    "django_mail_dnsname", 
    "django_mail_patch_dns", 
    "django_test_environment", 
    "django_user_model", 
    "django_username_field", 
    "doctest_namespace", 
    "get_client_with_url", 
    "httpserver", 
    "httpserver_ipv4", 
    "httpserver_ipv6", 
    "httpserver_listen_address", 
    "httpserver_ssl_context", 
    "live_server", 
    "mailoutbox", 
    "make_httpserver", 
    "make_httpserver_ipv4", 
    "make_httpserver_ipv6", 
    "monkeypatch", 
    "no_cover", 
    "pytestconfig", 
    "record_property", 
    "record_testsuite_property", 
    "record_xml_attribute", 
    "recwarn", 
    "rf", 
    "settings", 
    "tmp_path", 
    "tmp_path_factory", 
    "tmpdir", 
    "tmpdir_factory", 
    "transactional_db"
]

@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        email='test@test.com',
        password='12345678',
    )

@pytest.fixture
def image(db):
    with open('tests/assets/preview.jpg', 'rb') as img:
        file = SimpleUploadedFile(
            name='preview.jpg', 
            content=img.read(), 
            content_type='image/jpeg'
        )
        food_image = FoodImage(image=file)
        
        return food_image

@pytest.fixture
def image_file(db):
    with open('tests/assets/preview.jpg', 'rb') as img:
        file = SimpleUploadedFile(
            name='preview.jpg', 
            content=img.read(), 
            content_type='image/jpeg'
        )
        return file

@pytest.fixture
def valid_image_data(db, image_file):
    return {
        'image_data': 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode(),
    }

@pytest.fixture
def product(db):
    return Products.objects.create(name='Test Product')

@pytest.fixture
def category(db):
    return Category.objects.create(name='Category1')

@pytest.fixture
def product1(db, category):
    return Products.objects.create(name='Product1', category=category)

@pytest.fixture
def product2(db, category):
    return Products.objects.create(name='Product2', category=category)
