import pytest
from django.urls import reverse
from django.test import Client


def test_home_view_return_200():
    c = Client()
    rev = reverse('home')
    res = c.get(rev)
    assert res.status_code == 200
