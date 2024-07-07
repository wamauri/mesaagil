import pytest
from django.urls import reverse
from django.test import Client


class TestViews:
    def setup_method(self, test_method):
        self.c = Client()

    def teardown_method(self, test_method):
        pass

    def test_home_view_return_200(self):
        url = reverse('home')
        res = self.c.get(url)
        assert res.status_code == 200

    def test_overview_view_return_200(self):
        url = reverse('overview')
        res = self.c.get(url)
        assert res.status_code == 200

    def test_dashboard_view_return_200(self):
        url = reverse('dashboard')
        res = self.c.get(url)
        print(dir(res))
        assert res.status_code == 200
